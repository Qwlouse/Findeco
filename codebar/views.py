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

from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout

def home(request, path):
    return render_to_response("index.html", {"pagename":"Root"},
        context_instance=RequestContext(request))

def load_index(path):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def load_graph_data(graph_data_type, path):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def load_microblogging(path, select_id, microblogging_load_type):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def load_text(path):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def load_user_info(name):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def load_user_settings(request):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

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
            return json.dumps({
                'success':True,
                'userData':get_user_data(user)
            })
        else:
            return json.dumps({
                'success':False,
                'error':'DisabledAccount.',
                'userData':get_user_data(user)
            })
    else:
        return json.dumps({
            'success':False,
            'error':'InvalidLogin'
        })

def logout(request):
    django_logout(request)
    return json.dumps({'success':True})

def mark_node(path, mark_type):
    """
    If an argument is marked but wasn't created at this location it must be copied and the marking is to apply to the
    copied one.
    """
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def store_microblog_post(path):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def store_settings(request):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)

def store_text(path):
    # Backend foo
    data = "Yes, we can!"
    return json.dumps(data)