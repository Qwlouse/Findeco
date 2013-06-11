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
from __future__ import division, print_function, unicode_literals
from django.db.models import Q
from findeco.view_helpers import assert_node_for_path, assert_active_user
from findeco.view_helpers import assert_authentication, assert_post_parameters
from findeco.view_helpers import ViewErrorHandling
from models import create_post, Post
import node_storage as backend
from findeco.view_helpers import json_response
from time import mktime


def convert_response_list(post_list):
    response_list = []
    for post in post_list:
        authors = [{'displayName': post.author.username}]
        if post.is_reference_to:
            authors.append(
                {'displayName': post.is_reference_to.author.username})
        response_list.append(
            {'microblogText': post.text,
             'authorGroup': authors,
             'microblogTime': int(mktime(post.time.timetuple())),
             'microblogID': post.pk})
    return response_list


def convert_long_urls(request):
    """
    This function removes the unnecessary part from urls which are copy&pasted from the url field of the browser.
    """
    hostname = request.META['HTTP_HOST']
    text = request.POST['microblogText']
    text = text.replace("https://" + hostname + "/#", "")
    text = text.replace("http://" + hostname + "/#", "")
    text = text.replace(hostname + "/#", "")
    return text


@ViewErrorHandling
def load_microblogging(request, path, select_id, microblogging_load_type):
    # TODO refactor and optimize this method
    node = assert_node_for_path(path)
    if not select_id:  # Get latest posts
        posts = list(reversed(node.microblogging_references.order_by('-time').
                              prefetch_related('author', 'is_reference_to')[:20]))
    else:
        if microblogging_load_type == "newer":
            posts = list(node.microblogging_references.filter(id__gt=select_id).
                         order_by('time').prefetch_related('author', 'is_reference_to')[:20])
        else:  # older
            posts = list(reversed(node.microblogging_references.filter(id__lt=select_id).
                                  order_by('-time').prefetch_related('author', 'is_reference_to')[:20]))
    return json_response({
        'loadMicrobloggingResponse': convert_response_list(reversed(posts))})


@ViewErrorHandling
def load_timeline(request, name, select_id, microblogging_load_type):
    """
    Use this function to get the timeline for the given user.

    Referenced posts will show up in the timeline as the originals do.
    Hiding of the original posts for a tidy
    timeline should be done in the frontend due to performance reasons.
    """
    named_user = assert_active_user(name)

    if named_user == request.user:
        followed = Q(author__in=named_user.profile.followees.all())
    else:
        followed = Q(author=named_user)
    own = Q(author=named_user)
    if not select_id:  # Get latest posts
        feed = Post.objects.filter(followed | own).\
            order_by('-time').distinct().prefetch_related('author', 'is_reference_to')[:20]
        return json_response({
            'loadMicrobloggingResponse': convert_response_list(feed)})
    else:
        if microblogging_load_type == "newer":
            startpoint = Q(id__gt=select_id)
        else:  # older
            startpoint = Q(id__lt=select_id)
        feed = Post.objects.filter(followed | own)
        feed = feed.filter(startpoint).order_by('time').distinct()
        feed = feed.prefetch_related('author', 'is_reference_to')[:20]
        return json_response({
            'loadMicrobloggingResponse': convert_response_list(reversed(feed))})


@ViewErrorHandling
def load_collection(request, select_id, microblogging_load_type, only_author=False):
    """
    Use this function to get a collection of blogposts regarding nodes
    which are followed by the user.
    """
    if not select_id:  # Get latest posts
        feed = Post.objects.filter(node_references__votes__user=request.user).order_by('-time')
        if only_author:
            feed = feed.filter(node_references__text__authors=request.user)
        feed = feed.prefetch_related('author', 'is_reference_to')[:20]
        return json_response({'loadMicrobloggingResponse': convert_response_list(feed)})
    else:
        if microblogging_load_type == "newer":
            startpoint = Q(id__gt=select_id)
            print("newer, select-id=" + str(select_id))
        else:  # older
            startpoint = Q(id__lt=select_id)
            print("older, select-id=" + str(select_id))
        feed = Post.objects.filter(node_references__votes__user=request.user).filter(startpoint)
        if only_author:
            feed = feed.filter(node_references__text__authors=request.user)
        feed = feed.order_by('time').prefetch_related('author', 'is_reference_to')[:20]
        return json_response({'loadMicrobloggingResponse': convert_response_list(reversed(feed))})


@ViewErrorHandling
def store_microblog_post(request, path):
    assert_authentication(request)
    assert_post_parameters(request, ['microblogText'])
    post_text = convert_long_urls(request)
    create_post(post_text, request.user, path)
    return json_response({'storeMicrobloggingResponse': {}})