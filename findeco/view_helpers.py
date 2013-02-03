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
from django.contrib.auth.models import Permission
from django.http import HttpResponse
import functools
import json

import node_storage as backend
from node_storage import Vote, get_node_for_path
from node_storage.factory import create_argument
from node_storage.models import NodeOrder, Argument
from node_storage.path_helpers import get_good_path_for_structure_node
from .paths import parse_suffix
from .api_validation import validate_response

def json_response(data):
    return HttpResponse(json.dumps(data), mimetype='application/json')

def json_error_response(title, message):
    response = {'errorResponse':{
        'errorTitle':title,
        'errorMessage':message,
        }}
    return json_response(response)

def ValidPaths(*allowed_path_types):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(request, path, *args, **kwargs):
            _, path_type = parse_suffix(path)

            if 'arg_id' in path_type:
                path_type = 'Argument'
            elif 'arg_type' in path_type:
                path_type = 'ArgumentCategory'
            elif 'slot' in path_type:
                path_type = 'Slot'
            else:
                path_type = 'StructureNode'
            if path_type not in allowed_path_types:
                return json_error_response('IllegalPath',
                    "%s can be called only for %s but was called with %s"%(
                        f.__name__, allowed_path_types, path_type))
                #noinspection PyCallingNonCallable
            response = f(request, path, *args, **kwargs)
            validate_response(response.content, f.__name__)
            return response
        return wrapped
    return wrapper

def create_user_info(user):
    user_info = dict(
        displayName = user.username,
        description = user.profile.description,
        followers = [{'displayName':u.user.username} for u in user.profile.followers.all()],
        followees = [{'displayName':u.user.username} for u in user.profile.followees.all()]
    )
    return user_info

def create_user_settings(user):
    rights = 0
    if user.groups.filter(name='texters').count() > 0:
        rights += 1
    if user.groups.filter(name='voters').count() > 0:
        rights += 2
    if user.is_superuser:
        rights += 4
    user_settings = dict(
        blockedUsers = [{'displayName':u.user.username} for u in user.profile.blocked.all()],
        userRights = rights
    )
    return user_settings

def create_index_node_for_slot(slot):
    favorit = backend.get_favorite_if_slot(slot) ##optimization: switch to get_favorit_for_slot that also returns the index
    index_node = dict(
        shortTitle = slot.title,
        fullTitle = favorit.title,
        index = favorit.get_index(slot),
        authorGroup = [create_user_info(a) for a in favorit.text.authors.all()]
    )
    return index_node


def create_index_node_for_argument(argument, node):
    index_node = dict(
        shortTitle = Argument.long_arg_type(argument.arg_type),
        fullTitle = argument.title,
        index = argument.index,
        authorGroup = [create_user_info(a) for a in argument.text.authors.all()]
    )
    return index_node

def build_text(node, depth=2):
    depth = min(depth, 6)
    text = "=" * depth + node.title + "=" * depth + "\n" + node.text.text
    for slot in node.children.all():
        favorite = backend.get_favorite_if_slot(slot)
        text += "\n\n" + build_text(favorite, depth + 1)
    return text


def create_graph_data_node_for_structure_node(node, slot=None, path=None, slot_path=None):
    if slot_path:
        slot = get_node_for_path(slot_path)

    if not path:
        path = get_good_path_for_structure_node(node, slot, slot_path)

    if slot:
        if not slot_path:
            slot_path = slot.get_a_path()
        origin_group = [slot_path + '.' + str(n.get_index(slot)) for n in node.sources.filter(parents__in=[slot]).all()]
        origin_group += [n.get_a_path() for n in node.sources.exclude(parents__in=[slot]).all()]
    else:
        origin_group = [n.get_a_path() for n in node.sources.all()]

    graph_data_node = dict(
        path=path,
        authorGroup=[create_user_info(a) for a in node.text.authors.all()],
        follows=node.votes.count(),
        unFollows=node.get_unfollows(),
        newFollows=node.get_newfollows(),
        originGroup=[o.rstrip('/') for o in origin_group]
    )
    return graph_data_node

def store_structure_node(path, wiki_text, author):
    slot_path = path.rsplit('.',1)[0]
    slot = get_node_for_path(slot_path)
    structure = backend.parse(wiki_text, None)
    structure_node = backend.create_structure_from_structure_node_schema(structure, slot, [author])
    # add auto follow
    v = Vote(user=author)
    v.save()
    v.nodes.add(structure_node)
    return structure_node, get_good_path_for_structure_node(structure_node, slot, slot_path)

def store_argument(path, arg_text, arg_type, author):
    node = get_node_for_path(path)
    title = backend.get_title_from_text(arg_text)
    original_argument = create_argument(node, arg_type, title, arg_text, [author])
    for d in traverse_derivates(node):
        new_argument=create_argument(d, arg_type, title, arg_text, [author])
        original_argument.add_derivate(new_argument)
    return path + "." + arg_type + "." + str(node.arguments.count())

def store_derivate(path, arg_text, arg_type, derivate_wiki_text, author):
    new_node, new_path = store_structure_node(path, derivate_wiki_text, author)
    node = get_node_for_path(path)
    node.add_derivate(new_node, type=arg_type, title=backend.get_title_from_text(arg_text), text=arg_text, authors=[author])
    return new_path

def traverse_derivates_subset(node, subset):
    der_list = list((node.derivates.all() & subset).all())
    while len(der_list) > 0:
        derivate = der_list.pop()
        der_list += list((derivate.derivates.all() & subset).all())
        yield derivate

def traverse_derivates(node):
    der_list = list(node.derivates.all())
    while len(der_list) > 0:
        derivate = der_list.pop()
        der_list += list(derivate.derivates.all())
        yield derivate

def get_permission(name):
    a, _, n = name.partition('.')
    return Permission.objects.get(content_type__app_label=a, codename=n)