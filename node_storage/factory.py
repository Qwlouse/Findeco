#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
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
# #############################################################################
#
# #############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################
from django.contrib.auth.models import User, Group
from findeco.paths import parse_path
from models import Node, Text, Vote, Argument, SpamFlag
from node_storage import get_node_for_path, IllegalPath, get_root_node
from validation import valid_title, general_heading


def create_slot(short_title):
    slot = Node(node_type=Node.SLOT, title=short_title)
    slot.save()
    return slot


def create_structureNode(long_title, text="", authors=(), validate=False):
    if validate and not valid_title.match(long_title):
        raise ValueError('Invalid title "{}"'.format(long_title))
    if validate:
        head = general_heading.match(text)
        if head is not None:
            raise ValueError('Headings are not allowed in text: {}'
                             .format(head.group()))
    structure = Node(node_type=Node.STRUCTURE_NODE, title=long_title)
    structure.save()
    text_obj = Text(node=structure, text=text)
    text_obj.save()
    for author in authors:
        text_obj.authors.add(author)
    text_obj.save()
    return structure


def create_textNode(long_title, text="", authors=()):
    text_node = Node()
    text_node.node_type = Node.TEXTNODE
    text_node.title = long_title
    text_node.save()
    text_obj = Text()
    text_obj.node = text_node
    text_obj.text = text
    text_obj.save()
    for author in authors:
        text_obj.authors.add(author)
    text_obj.save()
    return text_node


def create_vote(voter, nodes):
    v = Vote()
    v.user = voter
    v.save()
    for node in nodes:
        v.nodes.add(node)
    v.save()
    for node in nodes:
        node.update_favorite_for_all_parents()
    return v


def create_spam_flag(voter, nodes):
    v = None
    for node in nodes:
        v = SpamFlag()
        v.user = voter
        v.node = node
        v.save()
    return v


def create_argument(node, arg_type='n', title="", text="", authors=()):
    arg_type = Argument.short_arg_type(arg_type)
    arg = Argument(arg_type=arg_type, title=title)
    arg.node_type = Node.ARGUMENT
    arg.concerns = node
    arg.save()
    text_obj = Text(node=arg, text=text)
    text_obj.save()
    for author in authors:
        text_obj.authors.add(author)
    text_obj.save()
    return arg


def create_user(username, description="", mail="a@bc.de", password=None,
                groups=()):
    if password:
        new_user = User.objects.create_user(username, mail, password)
    else:
        new_user = User(username=username, email=mail)
        new_user.save()
    for group in groups:
        Group.objects.get(name=group).user_set.add(new_user)

    new_user.profile.description = description
    new_user.profile.save()

    return new_user


def create_nodes_for_path(path, authors=()):
    nodes, last = parse_path(path)
    current_node = get_root_node()
    current_path = ""
    for short_title, index in nodes:
        # slot
        current_path += '/' + short_title
        try:
            current_slot = get_node_for_path(current_path)
        except IllegalPath:
            current_slot = create_slot(short_title)
            current_node.append_child(current_slot)

        # alternatives
        current_path += '.' + str(index)
        try:
            current_node = get_node_for_path(current_path)
        except IllegalPath:
            if current_slot.child_order_set.count() == 0:
                highest_index = 0
            else:
                highest_index = current_slot.child_order_set.order_by(
                    'position')[0].position

            for i in range(highest_index, index):
                current_node = create_structureNode(short_title + '_long',
                                                    authors=authors)
                current_slot.append_child(current_node)

    return current_node