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
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from findeco.view_helpers import create_graph_data_node_for_structure_node

import node_storage as backend
from node_storage.factory import create_argument
from .paths import parse_suffix
from .view_helpers import ValidPaths, json_error_response, json_response
from .view_helpers import store_structure_node, store_argument, store_derivate
from .view_helpers import create_index_node_for_slot, create_user_info
from .view_helpers import create_user_settings, create_index_node_for_argument
from .view_helpers import traverse_derivates_subset, traverse_derivates
from .view_helpers import build_text

def home(request, path):
    with open("static/index.html", 'r') as index_html_file:
        return HttpResponse(index_html_file.read(), mimetype='text/html')

@ValidPaths("StructureNode")
def load_index(request, path):
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('NonExistingNode','Illegal Path: ' + path)
    slot_list = backend.get_ordered_children_for(node)
    index_nodes = [create_index_node_for_slot(slot) for slot in slot_list]
    return json_response({'loadIndexResponse':index_nodes})

@ValidPaths("StructureNode")
def load_argument_index(request, path):
    prefix, path_type = parse_suffix(path)
    try:
        node = backend.get_node_for_path(prefix)
    except backend.IllegalPath:
        return json_error_response('NonExistingNode','Illegal Path: ' + path)
    data = [create_index_node_for_argument(a, node) for a in node.arguments.order_by('index')]
    return json_response({'loadIndexResponse':data})

@ValidPaths("StructureNode")
def load_graph_data(request, path, graph_data_type):
    if not path.strip('/'):# root node!
        nodes = [backend.get_root_node()]
        related_nodes = []
    else:
        slot_path = path.rsplit('.',1)[0]
        try:
            slot = backend.get_node_for_path(slot_path)
        except backend.IllegalPath:
            return json_error_response('NonExistingNode','Could not find slot: ' + slot_path + ' for node ' + path)
        nodes = backend.get_ordered_children_for(slot)
        sources = Q(derivates__in=nodes)
        derivates =Q(sources__in=nodes)
        related_nodes = backend.Node.objects.filter(sources | derivates).\
                                             exclude(id__in=[n.id for n in nodes]).distinct().all()

    graph_data_children = [create_graph_data_node_for_structure_node(n) for n in nodes]
    graph_data_related = [create_graph_data_node_for_structure_node(n) for n in related_nodes]
    data = {'graphDataChildren':graph_data_children,
            'graphDataRelated':graph_data_related}
    return json_response({'loadGraphDataResponse':data})

@ValidPaths("StructureNode", "Argument")
def load_text(request, path):
    prefix, path_type = parse_suffix(path)
    try:
        node = backend.get_node_for_path(prefix)
    except backend.IllegalPath:
        return json_error_response('IllegalPath','Illegal Path: '+path)

    paragraphs = [{'wikiText': "=" + node.title + "=\n" + node.text.text,
                   'path': path,
                   'isFollowing': node.votes.filter(user=request.user.id).count()>0,
                   'authorGroup': [create_user_info(a) for a in node.text.authors.all()]}]
    for slot in backend.get_ordered_children_for(node):
        favorite = backend.get_favorite_if_slot(slot)
        paragraphs.append({'wikiText': build_text(favorite, depth=2),
                           'path': path + "/" + slot.title + "." + str(favorite.get_index(slot)),
                           'isFollowing': favorite.votes.filter(user=request.user.id).count()>0,
                           'authorGroup': [create_user_info(a) for a in favorite.text.authors.all()]})
    isFollowing = 0
    v = node.votes.filter(user=request.user.id)
    if v.count() > 0:
        v = v[0]
        isFollowing = 1 # at least transitive follow
        if v.nodes.order_by('id')[0] == node:
            isFollowing = 2 # explicit follow

    return json_response({
        'loadTextResponse':{
            'paragraphs': paragraphs,
            'isFollowing': isFollowing}})

def load_user_info(request, name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return json_error_response('UnknownUser', "User '%s' not found!"%name)
    user_info = create_user_info(user)
    return json_response({
        'loadUserInfoResponse':{
            'userInfo':user_info
        }})

def load_user_settings(request):
    if not request.user.is_authenticated():
        return json_error_response('NeedsAuthentication',
            "You need to be logged in to load user settings.")
    user = User.objects.get(id=request.user.id)
    return json_response({'loadUserSettingsResponse':{
        'userInfo':create_user_info(user),
        'userSettings':create_user_settings(user)
        }})

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return json_response({
                'loginResponse':{
                    'userInfo':create_user_info(user),
                    'userSettings':create_user_settings(user)
                }})
        else:
            return json_error_response('DisabledAccount',"Account '%s' is deactivated"%username)
    else:
        return json_error_response('InvalidLogin', "Username or password wrong.")

def logout(request):
    django_logout(request)
    return json_response({'logoutResponse':{
        # TODO random farewell message
        'farewellMessage':"Didel dadel dana, ab geht's ins Nirvana."
    }})

@ValidPaths("StructureNode", "Argument")
def flag_node(request, path):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to flag node.")
    if not request.user.has_perm('node_storage.add_spamflag'):
        return json_error_response('PermissionDenied', "You do not have the permission to flag " + path + ".")
    user = request.user
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal Path','Illegal Path: '+path)

    marks = node.spam_flags.filter(user=user.id).all()
    if marks.count() == 0:
        new_mark = backend.SpamFlag()
        new_mark.node=node
        new_mark.user_id=request.user.id
        new_mark.save()
    return json_response({'markNodeResponse':{}})

@ValidPaths("StructureNode", "Argument")
def unflag_node(request, path):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to unflag node.")
    if not request.user.has_perm('node_storage.delete_spamflag'):
        return json_error_response('PermissionDenied', "You do not have the permission to unflag " + path + ".")
    user = request.user
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal Path','Illegal Path: '+path)

    marks = node.spam_flags.filter(user=user.id).all()
    if marks.count() == 1 :
        marks[0].delete()
    return json_response({'markNodeResponse':{}})

@ValidPaths("StructureNode", "Argument")
def follow_node(request, path):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to follow node.")
    user = request.user
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal Path','Illegal Path: '+path)

    marks = node.votes.filter(user=user.id).all()
    if marks.count() >= 1:
        mark = marks[0]
        if mark.head() != node:
            mark.nodes.remove(node)
            new_mark = backend.Vote()
            new_mark.user_id = request.user.id
            new_mark.save()
            new_mark.nodes.add(node)
            for n in traverse_derivates_subset(node, mark.nodes.all()):
                mark.nodes.remove(n)
                new_mark.nodes.add(n)
            mark.save()
            new_mark.save()
    else:
        mark = backend.Vote()
        mark.user_id = request.user.id
        mark.save()
        mark.nodes.add(node)
        for n in traverse_derivates(node):
            mark.nodes.add(n)
        mark.save()
    return json_response({'markNodeResponse':{}})

@ValidPaths("StructureNode", "Argument")
def unfollow_node(request, path):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to unfollow node.")
    user = request.user
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal Path','Illegal Path: '+path)

    marks = node.votes.filter(user=user.id).all()
    if marks.count() > 0:
        mark = marks[0]
        if mark.nodes.count() == 1:
            mark.delete()
        else:
            mark.nodes.remove(node)
            for n in traverse_derivates_subset(node, mark.nodes.all()):
                mark.nodes.remove(n)
            if mark.nodes.count() == 0:
                mark.delete()
    return json_response({'markNodeResponse':{}})


def store_settings(request):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to unfollow node.")
    user = User.objects.get(id=request.user.id)

    if not 'description' in request.POST:
        return json_error_response('MissingPOSTParameter', "The 'description' POST parameter is missing.")
    user.profile.description = request.POST['description']
    user.profile.save()
    if not 'displayName' in request.POST:
        return json_error_response('MissingPOSTParameter', "The 'displayName' POST parameter is missing.")
    display_name = request.POST['displayName']
    if display_name != user.username:
        is_available = User.objects.filter(username=display_name).count() == 0
        if not is_available:
            return json_error_response('NameNotAvailable', "The name '%s' is already taken."%display_name)
        else:
            user.username=display_name
    user.save()

    return json_response({'storeSettingsResponse':{}})

@ValidPaths("StructureNode")
def store_text(request, path):
    if not request.user.is_authenticated():
        return json_error_response('NotAuthenticated', "You need to be authenticated to store text.")
    user = request.user

    if not 'wikiText' in request.POST:
        return json_error_response('MissingPostParameter',
            'storeText is missing the wikiText POST parameter!')

    if not 'argumentType' in request.POST:
        if 'wikiTextAlternative' in request.POST:
            return json_error_response('MissingPostParameter',
            'You cannot use storeText to save a wikiTextAlternative without an argumentType!')
        # store new structure node
        _, new_path = store_structure_node(path, request.POST['wikiText'], user)

    elif 'wikiTextAlternative' not in request.POST:
        # store Argument
        new_path = store_argument(path, request.POST['wikiText'], request.POST['argumentType'], user)

    else:
        # store Argument and Derivate of structure Node
        arg_text = request.POST['wikiText']
        arg_type = request.POST['argumentType']
        derivate_wiki_text = request.POST['wikiTextAlternative']
        new_path = store_derivate(path, arg_text, arg_type, derivate_wiki_text, user)

    return json_response({'storeTextResponse':{'path':new_path}})