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
from models import Node, NodeOrder, Text, ArgumentOrder#, Argument
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
        argument_order = ArgumentOrder.objects.filter(node=node).\
                                     filter(position=last['arg_id']).prefetch_related('argument').all()
        if len(argument_order) != 1:
            raise IllegalPath(path)
        else:
            node = argument_order[0].argument
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
        return [i.argument for i in order if i.argument.arg_type == arg_type]
    else:
        return [i.argument for i in order]

def get_ordered_children_for(node):
    """
    Return a list of children for given node ordered by their position.
    """
    order = NodeOrder.objects.filter(parent=node).order_by('position')
    return [oN.child for oN in order]

def get_ordered_arguments_for(node):
    """
    Return a list of arguments for given node ordered by their position.
    """
    order = ArgumentOrder.objects.filter(node=node).order_by('position')
    return [ao.argument for ao in order]

#def get_similar_path(node, path=None):
#    """
#    Return a path to the node which corresponds to the given path if possible.
#    """
#    layers, last = parse_path(path)
#    candidates = [(get_root_node(), "")]
#    for title, pos_id in layers:
#        print("Beginn der Iteration. Es gibt "+str(len(candidates))+" Kandidaten.")
#        new_candidates = []
#        for candidate, part_path in candidates:
#            tmp_candidates = candidate.children.filter(text_object__text=title).prefetch_related('text_object').all()
#            if len(tmp_candidates) < 1: tmp_candidates = candidate.children.all()
#            print("Processing: "+title)
#            for c in tmp_candidates:
#                print(c)
#                print(c.node_type)
#                print(c.text_object.all())
#                if c == node: return part_path + "/" + c.text_object.all()[0].text
#                else: new_candidates.append((c, part_path + "/" + c.text_object.all()[0].text))
#            candidates = new_candidates
#            print("Zwischenschritt der Iteration. Es gibt "+str(len(candidates))+" Kandidaten.")
#            new_candidates = []
#            for candidate, part_path in candidates:
#                tmp_candidates = [o.child for o in NodeOrder.objects.filter(parent=candidate).\
#                                                                     filter(position=pos_id).\
#                                                                     prefetch_related('child').all()]
#                if len(tmp_candidates) < 1: tmp_candidates = candidate.children.all()
#                new_candidates += [(c, part_path + "." + str(
#                    NodeOrder.objects.filter(parent=candidate).filter(child=c).all()[0].position)) for c in
#                                   tmp_candidates]
#                for c in tmp_candidates:
#                    if c == node: return part_path + "." + str(
#                        NodeOrder.objects.filter(parent=candidate).filter(child=c).all()[0].position)
#                    else: new_candidates.append((c, part_path + "." + str(
#                        NodeOrder.objects.filter(parent=candidate).filter(child=c).all()[0].position)))
#                candidates = new_candidates
#    # This is reached if node is an argument
#    if 'arg_type' in last and 'arg_id' in last:
#        for candidate, part_path in candidates:
#            for argument, order in [(ao.argument, ao) for ao in ArgumentOrder.objects.filter(node=candidate).filter(
#                argument__in=candidate.arguments.filter(arg_type=last['arg_type']).all()).all()]:
#                if argument == node: return part_path + "." + argument.arg_type + "." + str(order.position)
#    return "Error: This node has no connection to the root."

#def get_path_parent(node, path):
#    """
#    Return the parent node which corresponds to the given path
#    """
#    layers, _ = parse_path(path)
#    if node.node_type == 'argument':
#       slot_candidates = []
#       for non_slot in node.concerns.all().prefetch_related('parents'):
#            slot_candidates += non_slot.parents.all()
#        slot_titles = Text.objects.filter(node__in=slot_candidates).filter(text=layers[-1][0]).prefetch_related('node').all()
#        if len(slot_titles) != 1:
#            return node.concerns.all()[0]
#        else:
#            return ArgumentOrder.objects.filter(node__in=slot_titles[0].node.children.all()).filter(argument=node).prefetch_related('node').all()[0].node
#    elif node.node_type == 'slot':
#        slot_candidates = []
#        for non_slot in node.parents.all().prefetch_related('parents'):
#            slot_candidates += non_slot.parents.all()
#        if len(layers) >= 2: slot_title = layers[-2][0]
#        elif len(layers) >= 1: slot_title = layers[-1][0]
#        else: return get_root_node()
#        parents = Text.objects.filter(node__in=slot_candidates).filter(text=slot_title).prefetch_related('node').all()
#        if len(parents) != 1:
#            return node.parents.all()[0]
#        else:
#            return NodeOrder.objects.filter(parent__in=parents[0].node.children.all()).filter(child=node).prefetch_related('parent').all()[0].parent
#    else:
#        parents = Text.objects.filter(node__in=node.parents.all()).filter(text=layers[-1][0]).prefetch_related('node').all()
#        if len(parents) != 1:
#            return node.parents.all()[0]
#        else:
#            return parents[0].node