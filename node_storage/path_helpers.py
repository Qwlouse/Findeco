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
from django.db.models import Count
from models import Node, NodeOrder, Text, ArgumentOrder, Argument
from findeco.paths import parse_path

def get_root_node():
    return Node.objects.filter(id=1)[0]

def get_node_for_path(path):
    """
    Return the node corresponding node to the given path.
    """
    node = get_root_node()
    layers, last = parse_path(path)
    for title, pos_id in layers:
        title_obj = Text.objects.filter(text=title).all()
        if len(title_obj) != 1:
            return node
        else:
            node_candidate = title_obj[0].node
            if node_candidate in node.children.all():
                node = NodeOrder.objects.filter(parent=node_candidate).filter(position=pos_id)[0].child
            else:
                return node
    if 'slot' in last:
        title_obj = Text.objects.filter(text=last['slot']).all()
        if len(title_obj) != 1:
            return node
        else:
            node_candidate = title_obj[0].node
            if node_candidate in node.children.all():
                node = node_candidate
            else:
                return node
    elif 'arg_type' in last and 'arg_id' in last:
        node = ArgumentOrder.objects.filter(node=node).filter(position=last['arg_id'])[0].argument
    return node

def get_favorite_if_slot(node):
    """
    Returns the favorite child if given a slot and returns node otherwise.
    """
    if node.node_type == 'slot':
        return node.children.annotate(num_votes=Count('votes')).order_by('-num_votes', '-pk')[0]
    else:
        return node

def get_arguments_for(node, arg_type='all'):
    """
    Return a list of arguments for node.
    arg_type can be one of: 'pro', 'con', 'neut', 'all'
    """
    order = ArgumentOrder.objects.filter(node=node).prefetch_related('argument')
    if arg_type != 'all':
        return [a for a in order.argument if order.argument.arg_type == arg_type]
    else:
        return [a for a in order.argument]

def get_ordered_children_for(node):
    """
    Return a list of children for given node ordered by their position.
    """
    order = NodeOrder.objects.filter(parent=node).order_by('position')
    return [oN.child for oN in order]

def get_similar_path(node, path=None):
    """
    Return a path to the node which corresponds to the given path if possible.
    """
    return "Not.1/Implemented.7"

def get_path_parent(node, path):
    """
    Return the parent node which corresponds to the given path
    """
    return None