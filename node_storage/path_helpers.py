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
from models import Node, NodeOrder, Argument

from findeco.paths import parse_path

class IllegalPath(Exception):
    pass

def get_root_node():
    return Node.objects.filter(id=1)[0]

def get_node_for_path(path):
    """
    Return the node corresponding node to the given path.
    """
    node = get_root_node()
    layers, last = parse_path(path)
    for title, pos_id in layers:
        children = node.children.filter(title=title).all()
        if len(children) != 1:
            raise IllegalPath(path)
        else:
            order = NodeOrder.objects.filter(parent__in=children).\
                                      filter(position=pos_id).prefetch_related('child').all()
            if len(order) != 1:
                raise IllegalPath(path)
            else:
                node = order[0].child
    if 'slot' in last:
        children = node.children.filter(title=last['slot']).all()
        if len(children) != 1:
            raise IllegalPath(path)
        else:
            node = children[0]
    elif 'arg_type' in last and 'arg_id' in last:
        argument_order = node.arguments.filter(index=last['arg_id']).prefetch_related('argument').all()
        if len(argument_order) != 1:
            raise IllegalPath(path)
        else:
            node = argument_order[0].argument
    return node

def get_favorite_if_slot(node):
    """
    Returns the favorite child if given a slot and returns node otherwise.
    """
    if node.node_type == Node.SLOT:
        return node.children.annotate(num_votes=Count('votes')).order_by('-num_votes', '-pk')[0]
    else:
        return node

def get_arguments_for(node, arg_type='all'):
    """
    Return a list of arguments for node.
    arg_type can be one of: 'pro', 'con', 'neut', 'all'
    """
#    order = ArgumentOrder.objects.filter(node=node).prefetch_related('argument')
#    if arg_type != 'all':
#        return [i.argument for i in order if i.argument.arg_type == Argument.short_arg_type(arg_type)]
#    else:
#        return [i.argument for i in order]

def get_ordered_children_for(node):
    """
    Return a list of children for given node ordered by their position.
    """
    order = NodeOrder.objects.filter(parent=node).order_by('position').prefetch_related('child')
    return [oN.child for oN in order]

def get_ordered_arguments_for(node):
    """
    Return a list of arguments for given node ordered by their position.
    """
#    order = ArgumentOrder.objects.filter(node=node).order_by('position')
#    return [ao.argument for ao in order]

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
        if node.id == 1: return ""
        no = NodeOrder.objects.filter(child=node)[0]
        slot = no.parent
        index = no.position
        return slot.get_a_path() + '.' + str(index)