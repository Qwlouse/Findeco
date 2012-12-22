#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
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

from codebar.paths import parse_suffix
import node_storage as backend

def json_response(data):
    return HttpResponse(json.dumps(data), mimetype='application/json')

def home(request, path):
    return render_to_response("index.html",
        context_instance=RequestContext(request))

def load_index(request, path):
    prefix, path_type = parse_suffix(path)
    if 'arg_id' in path_type:
        return json_response({'error':'NotPossibleForSingleArgument'})

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
    return json_response(data)

def load_graph_data(request, graph_data_type, path):
    # Backend foo
    data = "Yes, we can!"
    return json_response(data)

def load_text(request, path):
    prefix, path_type = parse_suffix(path)
    node = backend.get_favorite_if_slot(backend.get_node_for_path(prefix))
    paragraphs = []
    for slot in backend.get_ordered_children_for(node):
        best_choice = backend.get_favorite_if_slot(slot)
        paragraphs.append({'wikiText': best_choice.text_object.text,
                           'path': backend.get_similar_path(best_choice, path),
                           'isFollowing': len(
                               backend.Vote.objects.filter(nodes__in=best_choice).filter(user=request.user)),
                           'authorGroup': [{'displayName': a.username} for a in best_choice.text_object.authors]})
    return json_response({'paragraphs': paragraphs,
                          'index': node.get_index(),
                          'isFollowing': len(backend.Vote.objects.filter(nodes__in=node).filter(user=request.user))})

def load_user_info(request, name):
    # Backend foo
    data = "Yes, we can!"
    return json_response(data)

def load_user_settings(request):
    # Backend foo
    data = "Yes, we can!"
    return json_response(data)

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
    If an argument is marked but wasn't created at this location it must be copied and the marking is to apply to the
    copied one.
    """
    if request.user.is_authenticated:
        node = backend.get_node_for_path(path)
        if node:
            if mark_type in ("spam", "notspam"):
                mark = backend.SpamFlag()
            else: # follow or unfollow
                mark = backend.Vote()
            mark.user = request.user
            mark.nodes.create(node)
            mark.save()
            return json_response({'success':True})
    return json_response({'success':False}) # Should we specify the reason?

def store_settings(request):
    # Backend foo
    data = "Yes, we can!"
    return json_response(data)

def store_text(request, path):
    # Backend foo
    data = "Yes, we can!"
    return json_response(data)