#!/usr/bin/python
# coding=utf-8
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
################################################################################
from __future__ import division, print_function, unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

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
    title = models.CharField(max_length=150)
    node_type = models.CharField(max_length=1, choices=NODETYPE)

    def append_child(self, child):
        no = NodeOrder()
        no.parent = self
        no.child = child
        agg = NodeOrder.objects.filter(parent=self).aggregate(Max('position'))
        max_position = agg['position__max'] or 0
        no.position = max_position + 1
        no.save()

    def append_argument(self, argument):
        pass
#        no = ArgumentOrder()
#        no.node = self
#        no.argument = argument
#        agg = ArgumentOrder.objects.filter(node=self).aggregate(Max('position'))
#        max_position = agg['position__max'] or 0
#        no.position = max_position + 1
#        no.save()
#        for d in self.derivates.all():
#            d.append_argument(argument) # assumes no merges

    def add_derivate(self, argument, derivate):
        d = Derivation(argument=argument, source=self, derivate=derivate)
        d.save()
        self.append_argument(argument)
        for vote in Vote.objects.filter(nodes=self).all():
            vote.nodes.add(d.derivate)

    def __unicode__(self):
        return "id=%d, title=%s"%(self.id, self.title)

    def get_index(self, parent):
        """
        Return the index of this node within parent.
        """
        return NodeOrder.objects.get(parent=parent, child=self).position

    def get_a_path(self):
        """
        Returns a path which needn't be the only valid path to the node.
        """
        if self.pk == 1: return ""
        if self.node_type == Node.ARGUMENT:
            self_as_arg = Argument.objects.filter(argument_id=self.id).all()[0]
            return self_as_arg.concerns.get_a_path().strip('/') + '.' + self_as_arg.arg_type + '.' + str(self_as_arg.index)
        parent = self.parents.all()[0]
        return parent.get_a_path() +\
               (self.title if self.node_type == Node.SLOT else "." + str(self.get_index(parent)) + "/")

    def get_follows(self):
        return self.votes.count()

    def get_unfollows(self):
        return User.objects.filter(vote__nodes__in=self.sources.all()).exclude(vote__nodes__in=[self]).distinct().count()

    def get_newfollows(self):
        return self.votes.exclude(nodes__in=self.sources.all()).count()



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
        return {'pro':'pro',
                'neut':'neut',
                'con':'con',
                cls.PRO :'pro',
                cls.NEUT :'neut',
                cls.CON :'con'
           }[arg_type]

    @classmethod
    def short_arg_type(cls, arg_type):
        return {'pro' :cls.PRO,
                'neut':cls.NEUT,
                'con' :cls.CON,
                cls.PRO :cls.PRO,
                cls.NEUT:cls.NEUT,
                cls.CON :cls.CON
           }[arg_type]

    def save(self, *args, **kwargs):
        if self.index is None:
            self.index = self.concerns.arguments.count() + 1
        models.Model.save(self, *args, **kwargs)

    def __unicode__(self):
        return "id=%d, type=%s"%(self.id, self.arg_type)


class Text(models.Model):
    node = models.OneToOneField(Node, related_name="text")
    text = models.TextField()
    authors = models.ManyToManyField(
        User,
        related_name='author_in'
    )

    def __unicode__(self):
        return "id=%d, text=%s"%(self.id, self.text[:min(len(self.text), 30)])

############################# Relations ########################################
class Derivation(models.Model):
    derivate=models.ForeignKey(Node, related_name='source_order_set')
    source=models.ForeignKey(Node, related_name='derivative_order_set')
    argument=models.ForeignKey(Argument)

    class Meta:
        unique_together = (('source', 'derivate'), )

    def __unicode__(self):
        return "source_id=%d, derivate_id=%d, argument_id=%d"%(self.source_id,
                                                               self.derivate_id,
                                                               self.argument_id)

class NodeOrder(models.Model):
    child = models.ForeignKey(Node, related_name='parent_order_set')
    parent = models.ForeignKey(Node, related_name='child_order_set')
    position = models.IntegerField()

    class Meta:
        unique_together = (('parent', 'child'), )

    def __unicode__(self):
        return "pos=%d, child_id=%d, parent_id=%d"%(self.position,
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
        return "id=%d, user=%s"%(self.id, self.user.username)

class SpamFlag(models.Model):
    user = models.ForeignKey(User)
    node = models.ForeignKey(Node, related_name='spam_flags')
    def __unicode__(self):
        return "id=%d, user=%s"%(self.id, self.user.username)