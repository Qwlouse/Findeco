#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
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
        related_name="children",
        through='NodeOrder'
    )

    sources = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name="derivates",
        blank=True,
        through='Derivation'
    )

    type = models.CharField(max_length=1, choices=NODETYPE)

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
        related_name='arguments'
    )
    type = models.CharField(max_length=1, choices=ARGUMENTTYPE)

class Text(models.Model):
    node = models.ForeignKey(Node, related_name="text_object")
    text = models.TextField()
    authors = models.ManyToManyField(
        User,
        related_name='author_in'
    )

class Derivation(models.Model):
    source=models.ForeignKey(Node)
    derivate=models.ForeignKey(Node)
    argument=models.ForeignKey(Argument)

    class Meta:
        unique_together = (('source', 'derivate'), )

class NodeOrder(models.Model):
    parent = models.ForeignKey(Node)
    child = models.ForeignKey(Node)
    position = models.IntegerField()

    class Meta:
        unique_together = (('parent', 'child'), )

class Vote(models.Model):
    user = models.ForeignKey(User)
    nodes = models.ManyToManyField(
        Node,
        related_name='votes'
    )

class SpamFlag(models.Model):
    user = models.ForeignKey(User)
    nodes = models.ManyToManyField(
        Node,
        related_name='spam_flags'
    )
