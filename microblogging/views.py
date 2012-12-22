#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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
from django.db.models import Q
from models import Post, get_feed_for_user, create_post
from codebar.views import json_response
import node_storage as backend

def load_microblogging(request, path, select_id, microblogging_load_type):
    node = backend.get_node_for_path(path)
    if microblogging_load_type == "newer":
        startpoint = Q(pk__gt=select_id)
    else: # older
        startpoint = Q(pk__st=select_id)
    posts = Post.objects.filter(node_references__in=node).filter(startpoint)[:20]
    response_list = []
    for post in posts:
        authors = [{'displayName': post.author.username}]
        if post.is_reference_to: authors.append({'displayName': post.is_reference_to.author.username})
        response_list.append({'microBlogText': post.text,
                              'authorGroup': authors,
                              'microBlogTime': post.time,
                              'microBlogID': post.pk})
    return json_response(response_list)

def load_timeline(request):
    feed = get_feed_for_user(request.user)
    return json_response(feed)

def store_microblog_post(request, path):
    if request.method == 'POST':
        if request.user.is_authenticated:
            create_post(request.POST['microBlogText'], request.user)
            return json_response({'success': True})
    return json_response({'success': False})