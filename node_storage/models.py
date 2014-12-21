#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of Findeco.
#
# Findeco is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# Findeco is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Findeco. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#endregion #####################################################################
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Count


###################### Nodes, Arguments and Texts ##############################
class Node(models.Model):
    ARGUMENT = 'a'
    STRUCTURE_NODE = 'l'
    SLOT = 's'
    TEXTNODE = 't'
    NODETYPE = (
        (ARGUMENT, 'Argument'),
        (STRUCTURE_NODE, 'StructureNode'),
        (SLOT, 'Slot'),
        (TEXTNODE, 'TextNode')
    )

    parents = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='children',
        through='NodeOrder'
    )

    sources = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name="derivates",
        blank=True,
        through='Derivation'
    )
    favorite = models.ForeignKey('self', related_name='favorite_of', null=True,
                                 blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    node_type = models.CharField(max_length=1, choices=NODETYPE)

    def append_child(self, child):
        assert PathCache.objects.filter(node=self).count() > 0, \
            "You cannot add children to nodes that are not descendants of root."

        no = NodeOrder()
        no.parent = self
        no.child = child
        agg = NodeOrder.objects.filter(parent=self).aggregate(Max('position'))
        max_position = agg['position__max'] or 0
        no.position = max_position + 1
        no.save()
        self.update_favorite_and_invalidate_cache()
        for p in self.paths.all():
            child.recursive_add_new_path_to_parent(self, p.path)

    def recursive_add_new_path_to_parent(self, parent, path):
        if self.node_type == Node.SLOT:
            suffix = "/" + self.title
        else:
            suffix = "." + str(self.get_index(parent))
        new_path = path + suffix
        PathCache.objects.get_or_create(path=new_path.strip('/'), node=self)
        for c in self.children.all():
            c.recursive_add_new_path_to_parent(self, new_path)

    def add_derivate(self, derivate, arg_type=None, title="", text="",
                     authors=()):
        """
        Adds the given StructureNode as a derivative of this node.
        It takes care of transitive votes (but make sure to add the autofollow
        to the derivate BEFORE calling this function)
        It also copies all the arguments and generates a new derivation
        argument if the corresponding values are provided.
        Lastly it adds all the authors of this node to the derivate node.
        """
        for vote in self.votes.all():
            if derivate.votes.filter(user=vote.user).count() == 0:
                vote.nodes.add(derivate)
        for argument in self.arguments.all():
            copy_argument = Argument(title=argument.title, concerns=derivate,
                                     arg_type=argument.arg_type,
                                     node_type=Node.ARGUMENT)
            copy_argument.save()
            copy_argument_text_obj = Text(node=copy_argument,
                                          text=argument.text.text)
            copy_argument_text_obj.save()
            for author in argument.text.authors.all():
                copy_argument_text_obj.authors.add(author)
            copy_argument_text_obj.save()
            argument.add_derivate(copy_argument)

        for a in self.text.authors.all():
            derivate.text.authors.add(a)

        derivate.update_favorite_for_all_parents()
        if arg_type or title or text or len(authors) > 0:
            arg_type = Argument.short_arg_type(arg_type)
            source_argument = Argument(arg_type=arg_type, title=title,
                                       node_type=Node.ARGUMENT, concerns=self)
            source_argument.save()
            source_argument_text_obj = Text(node=source_argument, text=text)
            source_argument_text_obj.save()
            for author in authors:
                source_argument_text_obj.authors.add(author)
            source_argument_text_obj.save()
        else:
            source_argument = None
        d = Derivation(argument=source_argument, source=self, derivate=derivate)
        d.save()
        return source_argument

    def update_favorite_and_invalidate_cache(self):
        if self.children.count() == 0:
            return
        new_favorite = self.children.annotate(num_votes=Count('votes')).\
            order_by('-num_votes', '-pk')[0]
        if not self.favorite or new_favorite != self.favorite:
            self.favorite = new_favorite
            self.save()
            # TODO: optimize this
            invalid_paths = []
            for a in self.traverse_all_ancestors():
                invalid_paths += [p.path for p in a.paths.all()]
            TextCache.objects.filter(path__in=invalid_paths).delete()
            IndexCache.objects.filter(path__in=invalid_paths).delete()

    def update_favorite_for_all_parents(self):
        for p in self.parents.all():
            p.update_favorite_and_invalidate_cache()

    def __unicode__(self):
        return "id=%d, title=%s" % (self.id, self.title)

    def get_index(self, parent):
        """
        Return the index of this node within parent.
        """
        return NodeOrder.objects.get(parent=parent, child=self).position

    def traverse_all_ancestors(self):
        ancestors = list(self.parents.all())
        while len(ancestors) > 0:
            a = ancestors.pop()
            ancestors += list(a.parents.all())
            yield a

    def get_a_path(self):
        """
        Returns a path which needn't be the only valid path to the node.
        """
        paths = PathCache.objects.filter(node=self)
        if paths.count() > 0:
            return paths[0].path
        else:
            # Note: This should NEVER happen
            # but since it did we have a backup plan here
            # TODO Remove if we are absolutely sure that every node is in PathCache

            if self.parents.count() == 0:
                return ""
            if self.node_type == Node.ARGUMENT:
                self_as_arg = Argument.objects.filter(argument_id=self.id).all()[0]
                npath = self_as_arg.concerns.get_a_path().strip('/')
                return '%s.%s.%d' % (npath, self_as_arg.arg_type, self_as_arg.index)
            parent = self.parents.all()[0]
            if self.node_type == Node.SLOT:
                suffix = self.title
            else:
                suffix = "." + str(self.get_index(parent)) + "/"
            path = parent.get_a_path() + suffix
            # write to path
            PathCache.objects.create(node=self, path=path)
            return path

    def get_follows(self):
        return self.votes.count()

    def get_unfollows(self):
        return User.objects.filter(vote__nodes__in=self.sources.all()). \
            exclude(vote__nodes__in=[self]).distinct().count()

    def get_newfollows(self):
        return self.votes.exclude(nodes__in=self.sources.all()).count()

    def traverse_derivates(self, subset=None, condition=lambda n: True):
        if subset:
            der_list = list((self.derivates.all() & subset).all())
        else:
            der_list = list(self.derivates.all())
        while len(der_list) > 0:
            derivate = der_list.pop()
            if condition(derivate):
                if subset:
                    der_list += list((derivate.derivates.all() & subset).all())
                else:
                    der_list += list(derivate.derivates.all())
                yield derivate


class Argument(Node):
    PRO = 'p'
    CON = 'c'
    NEUT = 'n'
    ARGUMENTTYPE = (
        (PRO, 'pro'),
        (CON, 'con'),
        (NEUT, 'neut'),
    )

    arg_type = models.CharField(max_length=1, choices=ARGUMENTTYPE)

    concerns = models.ForeignKey(
        Node,
        related_name='arguments'
    )
    index = models.IntegerField()

    @classmethod
    def long_arg_type(cls, arg_type):
        return {'pro': 'pro',
                'neut': 'neut',
                'con': 'con',
                cls.PRO: 'pro',
                cls.NEUT: 'neut',
                cls.CON: 'con'
                }[arg_type]

    @classmethod
    def short_arg_type(cls, arg_type):
        return {None: cls.NEUT,
                'pro': cls.PRO,
                'neut': cls.NEUT,
                'con': cls.CON,
                cls.PRO: cls.PRO,
                cls.NEUT: cls.NEUT,
                cls.CON: cls.CON
                }[arg_type]

    def save(self, *args, **kwargs):
        new = False
        if self.index is None:
            # new Argument!
            self.index = self.concerns.arguments.count() + 1
            new = True

        models.Model.save(self, *args, **kwargs)
        if new:
            assert self.concerns.paths.count() > 0, \
                "You can only add arguments to descendants of root"
            for p in self.concerns.paths.all():
                path = '%s.%s.%d' % (p.path,
                                     self.long_arg_type(self.arg_type),
                                     self.index)
                PathCache.objects.create(path=path, node=self)

    def __unicode__(self):
        return "id=%d, type=%s" % (self.id, self.arg_type)


class Text(models.Model):
    node = models.OneToOneField(Node, related_name="text")
    text = models.TextField()
    authors = models.ManyToManyField(
        User,
        related_name='author_in'
    )

    def __unicode__(self):
        return "id=%d, text=%s" % (self.id, self.text[:min(len(self.text), 30)])


############################# Relations ########################################
class Derivation(models.Model):
    derivate = models.ForeignKey(Node, related_name='source_order_set')
    source = models.ForeignKey(Node, related_name='derivative_order_set')
    argument = models.ForeignKey(Argument, null=True, blank=True)

    class Meta:
        unique_together = (('source', 'derivate'), )

    def __unicode__(self):
        return "source_id=%d, derivate_id=%d, argument_id=%d" % \
               (self.source_id, self.derivate_id, self.argument_id)


class NodeOrder(models.Model):
    child = models.ForeignKey(Node, related_name='parent_order_set')
    parent = models.ForeignKey(Node, related_name='child_order_set')
    position = models.IntegerField()

    class Meta:
        unique_together = (('parent', 'child'), )

    def __unicode__(self):
        return "pos=%d, child_id=%d, parent_id=%d" % (self.position,
                                                      self.child_id,
                                                      self.parent_id)


################################# Votes ########################################
class Vote(models.Model):
    user = models.ForeignKey(User)
    nodes = models.ManyToManyField(
        Node,
        related_name='votes'
    )

    def head(self):
        return self.nodes.order_by('id').all()[0]

    def __unicode__(self):
        return "id=%d, user=%s" % (self.id, self.user.username)


class SpamFlag(models.Model):
    user = models.ForeignKey(User)
    node = models.ForeignKey(Node, related_name='spam_flags')

    def __unicode__(self):
        return "id=%d, user=%s" % (self.id, self.user.username)


################################# Caches #######################################
class TextCache(models.Model):
    path = models.CharField(max_length=250, primary_key=True)
    paragraphs = models.TextField()


class IndexCache(models.Model):
    path = models.CharField(max_length=250, primary_key=True)
    index_nodes = models.TextField()


class PathCache(models.Model):
    path = models.CharField(max_length=250, primary_key=True)
    node = models.ForeignKey(Node, related_name='paths')