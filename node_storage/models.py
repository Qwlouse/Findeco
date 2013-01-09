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

#Todo get a path to root (see path_helpers)

NODETYPE = (
    ('a', 'argument'),
    ('l', 'structureNode'),
    ('s', 'slot'),
    ('t', 'textNode')
    )
class Node(models.Model):
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
        no = ArgumentOrder()
        no.node = self
        no.argument = argument
        agg = ArgumentOrder.objects.filter(node=self).aggregate(Max('position'))
        max_position = agg['position__max'] or 0
        no.position = max_position + 1
        no.save()

    def __unicode__(self):
        return "id=%d, type=%s"%(self.id, self.node_type)

    def get_short_title(self, parent): # This is deprecated
        """
        Return the short title used to identify this node in parent.
        """
        pass

    def get_full_title(self):
        """
        Return the full title of this node.
        """
        pass

    def get_index(self, parent):
        """
        Return the index of this node within parent.
        """
        pass

ARGUMENTTYPE = (
    ('p', 'pro'),
    ('c', 'con'),
    ('n', 'neut'),
)
class Argument(Node):
    concerns = models.ManyToManyField(
        Node,
        related_name='arguments',
        through='ArgumentOrder'
    )
    arg_type = models.CharField(max_length=1, choices=ARGUMENTTYPE)
    def __unicode__(self):
        return "id=%d, type=%s"%(self.id, self.arg_type)

class Text(models.Model):
    node = models.ForeignKey(Node, related_name="text_object")
    text = models.TextField()
    authors = models.ManyToManyField(
        User,
        related_name='author_in'
    )

    def __unicode__(self):
        return "id=%d, text=%s"%(self.id, self.text)

class Derivation(models.Model):
    source=models.ForeignKey(Node, related_name='derivative_order_set')
    derivate=models.ForeignKey(Node, related_name='source_order_set')
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

class ArgumentOrder(models.Model):
    argument = models.ForeignKey(Argument, related_name='node_order_set')
    node = models.ForeignKey(Node, related_name='argument_order_set')
    position = models.IntegerField()

    class Meta:
        unique_together = (('argument', 'node'), )

    def __unicode__(self):
        return "pos=%d, argument_id=%d, node_id=%d"%(self.position,
                                                     self.argument_id,
                                                     self.node_id)


class Vote(models.Model):
    user = models.ForeignKey(User)
    nodes = models.ManyToManyField(
        Node,
        related_name='votes'
    )

    def __unicode__(self):
        return "id=%d, user=%s"%(self.id, self.user.username)

class SpamFlag(models.Model):
    user = models.ForeignKey(User)
    nodes = models.ManyToManyField(
        Node,
        related_name='spam_flags'
    )
    def __unicode__(self):
        return "id=%d, user=%s"%(self.id, self.user.username)