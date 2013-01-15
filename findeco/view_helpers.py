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
import json
from django.http import HttpResponse
from findeco.paths import parse_suffix
from api_validation import validate_response
import node_storage as backend

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
                return json_error_response('Invalid path for %s'%f.__name__,
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

def create_index_node_for_slot(slot):
    favorit = backend.get_favorite_if_slot(slot) ##optimization: switch to get_favorit_for_slot that also returns the index
    index_node = dict(
        shortTitle = slot.title,
        fullTitle = favorit.title,
        index = favorit.get_index(slot),
        authorGroup = [create_user_info(a) for a in favorit.text.authors.all()]
    )
    return index_node
