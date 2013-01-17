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
from django.shortcuts import render_to_response
from django.template import RequestContext

from findeco.paths import parse_suffix
from findeco.view_helpers import ValidPaths, json_error_response, json_response, create_index_node_for_slot, create_user_info, create_user_settings, create_index_node_for_argument
import node_storage as backend

def home(request, path):
    return render_to_response("main.html",
        {"path": path},
        context_instance=RequestContext(request))

@ValidPaths("StructureNode")
def load_index(request, path):
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('NonExistingNode','Illegal Path: '+path)
    slot_list = backend.get_ordered_children_for(node)
    index_nodes = [create_index_node_for_slot(slot) for slot in slot_list]
    return json_response({'loadIndexResponse':index_nodes})

@ValidPaths("Argument")
def load_argument_index(request, path):
    prefix, path_type = parse_suffix(path)
    try:
        node = backend.get_node_for_path(prefix)
    except backend.IllegalPath:
        return json_error_response('IllegalPath','Illegal Path: '+path)

    argument_list = backend.get_ordered_arguments_for(node)
    # Backend foo
    data = [create_index_node_for_argument(a, node) for a in argument_list]
    return json_response({'loadIndexResponse':data})

@ValidPaths("StructureNode")
def load_graph_data(request, path, graph_data_type):
    # This is an example
    user = {
        'displayName':"Max Mustermann",
        'description':"string",
        'followers':[],
        'followees':[]
    }
    data = {'graphDataChildren':[{'path':"Bla.4/blubb.3",
                                  'authorGroup':[user],
                                  'follows':210,
                                  'unFollows':136,
                                  'newFollows':13,
                                  'originGroup':["Bla.4/blubb.3"]},
                                 {'path':"Bla.4/blubb.7",
                                  'authorGroup':[user],
                                  'follows':10,
                                  'unFollows':536,
                                  'newFollows':500,
                                  'originGroup':["Bla.4/blubb.4"]}],
            'graphDataRelated':[{'path':"Bla.4/blubb.14",
                                 'authorGroup':[user],
                                 'follows':110,
                                 'unFollows':176,
                                 'newFollows':19,
                                 'originGroup':["Bla.4/blubb.7"]}]}
    return json_response({'loadGraphDataResponse':data})

@ValidPaths("StructureNode", "Argument")
def load_text(request, path):
    prefix, path_type = parse_suffix(path)
    try:
        tmp_node = backend.get_node_for_path(prefix)
    except backend.IllegalPath:
        return json_error_response('IllegalPath','Illegal Path: '+path)
    node = backend.get_favorite_if_slot(tmp_node)
    if node == tmp_node: # not slot
        # this means the index in parent is the last integer in the prefix
        index = int(prefix.rsplit('.', 1)[-1] or '1')
    else: # slot
        index = node.get_index(tmp_node)

    paragraphs = [{'wikiText': node.text.text,
                   'path': path,
                   'isFollowing': node.votes.filter(user=request.user.id).count()>0,
                   'authorGroup': [create_user_info(a) for a in node.text.authors.all()]}]
    for slot in backend.get_ordered_children_for(node):
        favorite = backend.get_favorite_if_slot(slot)
        paragraphs.append({'wikiText': favorite.text.text,
                           'path': backend.get_similar_path(favorite, path),
                           'isFollowing': favorite.votes.filter(user=request.user.id).count()>0,
                           'authorGroup': [create_user_info(a) for a in favorite.text.authors.all()]})
    return json_response({
        'loadTextResponse':{
            'paragraphs': paragraphs,
            'isFollowing': node.votes.filter(user=request.user.id).count()>0}})

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
def mark_node(request, path, mark_type):
    """
    If an argument is marked but wasn't created at this location it must be
    copied and the marking is to apply to the copied one.
    """
    if not request.user.is_authenticated:
        return json_response({'error': "You're not authenticated."})
    user = request.user
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal Path','Illegal Path: '+path)
    if not node:
        return json_response({'error': "Invalid path."})

    if mark_type in ("spam", "notspam"):
        MarkClass = backend.SpamFlag
        marks = node.spam_flags.filter(user=user.id)
    else:# follow or unfollow
        MarkClass = backend.Vote
        marks = node.votes.filter(user=user.id)

    if marks.count() >= 1:
        #TODO: if a mark changes for a node that mark has to be copied
        mark = marks[0]
    else:
        mark = MarkClass()

    mark.user_id = request.user.id or 1 # TODO FIXME: Why can this be none during testing?
    mark.save()
    mark.nodes.add(node)
    mark.save()

    ## @jonny: I don't understand what this is for. Seems wrong to me:
#    if backend.get_similar_path(node, path) != path: #This means it is an argument which wasn't created here
#        a = backend.Argument()
#        a.concerns = backend.get_path_parent(node, path)
#        a.arg_type = node.arg_type
#        a.parents = node.parents
#        a.sources = node.sources
#        a.node_type = node.node_type
#        a.save()
#        t = backend.Text()
#        t.node = a
#        t.text = node.text_object.text
#        t.authors = node.text_object.authors
#        t.save()
#        node = a


    return json_response({'markNodeResponse':{}})



def store_settings(request):
    # Backend foo
    return json_response({})

def store_text(request, path):
    # Backend foo
    return json_response({})