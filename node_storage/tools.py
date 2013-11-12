#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from microblogging.models import Post
from node_storage.models import PathCache, TextCache, Vote, Argument, IndexCache, Node


def delete_node(node):
    paths = PathCache.objects.filter(node=node).all()
    TextCache.objects.filter(path__in=paths).delete()
    IndexCache.objects.filter(path__in=paths).delete()

    Post.objects.filter(node_references=node).delete()

    # delete derivation argument
    Argument.objects.filter(derivation__derivate=node).delete()
    # delete all derivatives
    derivates = list(node.derivates.all())
    parents = list(node.parents.all())
    node.delete()

    for d in derivates:
        try:
            derivate = Node.objects.get(id=d.id)
            delete_node(derivate)
        except ObjectDoesNotExist:
            pass

    for p in parents:
        try:
            parent = Node.objects.get(id=p.id)
            if parent.children.count() == 0:
                delete_node(parent)
            else:
                parent.update_favorite_and_invalidate_cache()
        except ObjectDoesNotExist:
            pass
    for n in Node.objects.filter(parents=None).exclude(title='ROOT').exclude(node_type=Node.ARGUMENT):
        delete_node(n)

    # remove all empty votes
    Vote.objects.filter(nodes=None).delete()
