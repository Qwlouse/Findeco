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
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

from findeco.paths import parse_suffix
import node_storage as backend

def json_response(data):
    return HttpResponse(json.dumps(data), mimetype='application/json')

def home(request, path):
    return render_to_response("main.html",
        {"path": path},
        context_instance=RequestContext(request))

def load_index(request, path):
    prefix, path_type = parse_suffix(path)
    if 'arg_id' in path_type:
        return json_response({'success':False,
                              'error':'NotPossibleForSingleArgument'})

    node = backend.get_node_for_path(prefix)

    if 'arg_type' in path_type:
        nodelist = backend.get_arguments_for(node, path_type['arg_type'])
    else:
        nodelist = backend.get_ordered_children_for(node)

    # Backend foo
    data = [{'shortTitle':n.get_short_title(),
             'fullTitle':n.get_full_title(),
             'index':n.get_index()
            } for n in nodelist]
    return json_response({'success':True,
                          'loadIndexResponse':data})

def load_graph_data(request, graph_data_type, path):
    # This is an example
    return json_response({'graphDataChildren':[{'index':1,
                                                'authorGroup':[{'displayName':"Max Mustermann"}],
                                                'follows':210,
                                                'unFollows':136,
                                                'newFollows':13,
                                                'origin':"Bla.4/blubb.3"},
                                               {'index':2,
                                                'authorGroup':[{'displayName':"Max Mustermann"}],
                                                'follows':10,
                                                'unFollows':536,
                                                'newFollows':500,
                                                'origin':"Bla.4/blubb.4"}],
                          'graphDataRelated':[{'index':14,
                                               'authorGroup':[{'displayName':"Max Mustermann"}],
                                               'follows':110,
                                               'unFollows':176,
                                               'newFollows':19,
                                               'origin':"Bla.4/blubb.7"}]})

def load_text(request, path):
    prefix, path_type = parse_suffix(path)
    tmp_node = backend.get_node_for_path(prefix)
    node = backend.get_favorite_if_slot(tmp_node)
    if node == tmp_node: # not slot
        # this means the index in parent is the last integer in the prefix
        index = int(prefix.rsplit('.', 1)[-1] or '1')
    else: # slot
        index = node.get_index(tmp_node)

    paragraphs = []
    for slot in backend.get_ordered_children_for(node):
        best_choice = backend.get_favorite_if_slot(slot)
        paragraphs.append({'wikiText': best_choice.text_object.text,
                           'path': backend.get_similar_path(best_choice, path),
                           'isFollowing': best_choice.votes.filter(user=request.user.id).count()>0,
                           'authorGroup': [{'displayName': a.username} for a in best_choice.text_object.authors]})
    return json_response({'paragraphs': paragraphs,
                          'index': index,
                          'isFollowing': node.votes.filter(user=request.user.id).count()>0})

def load_user_info(request, name):
    # This is an example
    return json_response({'displayName':"Maria Musterfrau",
                          'description':"== Blubb ==\nDie Beschreibung ist **toll**.",
                          'followers':[{'displayName':"Max Mustermann"},{'displayName':"Egon Mustermann"}],
                          'followees':[{'displayName':"Max Mustermann"},{'displayName':"Egon Mustermann"}]})

def load_user_settings(request):
    # This is an example
    return json_response({'success':True,
                          'userData':{'displayName':"Maria Musterfrau",
                                      'description':"== Blubb ==\nDie Beschreibung ist **toll**.",
                                      'followees':[{'displayName':"Max Mustermann"},{'displayName':"Egon Mustermann"}],
                                      'blockedUsers':[]}})

def get_user_data(user):
    return {
        'displayName':user.username,
        'description':user.profile.description,
        'followees':user.profile.followees.all(),
        'blockedUsers':[]
    }

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            django_login(request, user)
            return json_response({
                'success':True,
                'userData':get_user_data(user)
            })
        else:
            return json_response({
                'success':False,
                'error':'DisabledAccount.',
                'userData':get_user_data(user)
            })
    else:
        return json_response({
            'success':False,
            'error':'InvalidLogin'
        })

def logout(request):
    django_logout(request)
    return json_response({'success':True})

def mark_node(request, path, mark_type):
    """
    If an argument is marked but wasn't created at this location it must be
    copied and the marking is to apply to the copied one.
    """
    if not request.user.is_authenticated:
        return json_response({'success':False, 'error': "You're not authenticated."})
    user = request.user
    node = backend.get_node_for_path(path)
    if not node:
        return json_response({'success':False, 'error': "Invalid path."})

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


    return json_response({'success':True})



def store_settings(request):
    # Backend foo
    return json_response({'success':True})

def store_text(request, path):
    # Backend foo
    return json_response({'success':True})