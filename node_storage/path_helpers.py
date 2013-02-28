#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
from models import Node, NodeOrder, PathCache, Argument
import re


class IllegalPath(Exception):
    pass


def is_argument(path):
    return re.match(r".*\.(pro|neut|con|all)\.[0-9]+$", path) is not None


def get_root_node():
    return Node.objects.filter(id=1)[0]


def get_node_for_path(path):
    """
    Return the node corresponding node to the given path.
    """
    nodes = PathCache.objects.filter(path=path.strip('/'))
    if nodes.count() == 0:
        raise IllegalPath(path)

    node = nodes[0].node
    if is_argument(path):
        return Argument.objects.get(id=node.id)
    return node


def get_favorite_if_slot(node):
    """
    Returns the favorite child if given a slot and returns node otherwise.
    """
    if node.node_type == Node.SLOT:
        return node.favorite
    else:
        return node


def get_ordered_children_for(node):
    """
    Return a list of children for given node ordered by their position.
    """
    order = NodeOrder.objects.filter(parent=node).order_by(
        'position').prefetch_related('child')
    return [oN.child for oN in order]


def get_good_path_for_structure_node(node, slot=None, slot_path=None):
    """
    Get a path for a structure node. If a parent slot or it's path is given
    get the path that is relative to that path.
    """
    if slot:
        index = node.get_index(slot)
        return slot.get_a_path() + '.' + str(index)
    elif slot_path:
        slot = get_node_for_path(slot_path)
        return slot_path + '.' + str(node.get_index(slot))
    else:
        if node.id == 1:
            return ""
        no = NodeOrder.objects.filter(child=node)[0]
        slot = no.parent
        index = no.position
        return slot.get_a_path() + '.' + str(index)