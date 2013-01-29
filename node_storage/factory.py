#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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
from django.contrib.auth.models import User
from models import Node, Text, Vote, Argument, SpamFlag

def create_slot(short_title):
    slot = Node()
    slot.node_type = 'slot'
    slot.title = short_title
    slot.save()
    return slot

def create_structureNode(long_title, text="", authors=()):
    structure = Node()
    structure.node_type = 'structureNode'
    structure.title = long_title
    structure.save()
    text_obj = Text()
    text_obj.node = structure
    text_obj.text = text
    text_obj.save()
    for author in authors:
        text_obj.authors.add(author)
    text_obj.save()
    return structure

def create_textNode(long_title, text="", authors=()):
    text_node = Node()
    text_node.node_type = 'textNode'
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
    return v

def create_spam_flag(voter, nodes):
    v = SpamFlag()
    v.user = voter
    v.save()
    for node in nodes:
        v.nodes.add(node)
    v.save()
    return v

def create_argument(type='neut', title="", text="", authors=()):
    arg = Argument(arg_type=type, title=title)
    arg.node_type = 'argument'
    arg.save()
    text_obj = Text(node=arg, text=text)
    text_obj.save()
    for author in authors:
        text_obj.authors.add(author)
    text_obj.save()
    return arg

def create_user(username, description="", mail="a@bc.de", password=None):
    if password:
        new_user = User.objects.create_user(username, mail, password)
    else:
        new_user = User(username=username)
        new_user.save()

    new_user.profile.description = description
    new_user.profile.save()
    return new_user