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
from django.db.models import Q
from models import create_post, Post
from findeco.views import json_response, json_error_response
import node_storage as backend
from time import mktime

def convert_response_list(list):
    response_list = []
    for post in list:
        authors = [{'displayName': post.author.username}]
        if post.is_reference_to: authors.append({'displayName': post.is_reference_to.author.username})
        response_list.append({'microBlogText': post.text,
                              'authorGroup': authors,
                              'microBlogTime': int(mktime(post.time.timetuple())),
                              'microBlogID': post.pk})
    return response_list

def load_microblogging(request, path, select_id, microblogging_load_type):
    try:
        node = backend.get_node_for_path(path)
    except backend.IllegalPath:
        return json_error_response('Illegal path','Illegal path: '+path)
    if microblogging_load_type == "newer":
        startpoint = Q(id__gt=select_id)
    else: # older
        startpoint = Q(id__lt=select_id)
    posts = node.microblogging_references.filter(startpoint).prefetch_related('author', 'is_reference_to')[:20]
    return json_response({'loadMicrobloggingResponse':convert_response_list(posts)})

def load_timeline(request, select_id, microblogging_load_type):
    """
    Use this function to get the timeline for the given user.

    Referenced posts will show up in the timeline as the originals do. Hiding of the original posts for a tidy
    timeline should be done in the frontend due to performance resons.
    """
    followed = Q(author__profile__followers=request.user)
    own = Q(author = request.user)
    if microblogging_load_type == "newer":
        startpoint = Q(id__gt=select_id)
    else: # older
        startpoint = Q(id__lt=select_id)
    feed =  Post.objects.filter(followed | own).filter(startpoint).order_by('time').prefetch_related('author', 'is_reference_to')[:20]
    return json_response({'loadMicrobloggingResponse':convert_response_list(feed)})

def store_microblog_post(request, path):
    if request.method == 'POST':
        if request.user.is_authenticated:
            create_post(request.POST['microBlogText'], request.user)
            return json_response({})
        else:
            return json_error_response('Authentification reqired',"You need to be authenticated to store microblogging.")
    else:
        return json_error_response('Wrong method',"You must send a POST request to store microblogging.")