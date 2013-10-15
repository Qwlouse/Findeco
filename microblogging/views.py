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
from django.contrib.auth.models import User

from findeco.view_helpers import assert_node_for_path, assert_active_user
from findeco.view_helpers import assert_authentication, assert_post_parameters
from findeco.view_helpers import ViewErrorHandling
from microblogging.factory import create_post
from microblogging.view_helpers import *
from microblogging.view_helpers import get_microblogging_for_followed_nodes_query
from .models import Post
from findeco.view_helpers import json_response


@ViewErrorHandling
def load_microblogging_all(request):
    return microblogging_response(Q(), request.GET)


@ViewErrorHandling
def load_microblogging_for_node(request, path):
    node = assert_node_for_path(path)
    query = get_microblogging_for_node_query(node)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def load_microblogging_timeline(request, name):
    """
    Use this function to get the timeline for the given user.
    """
    named_user = assert_active_user(name)
    query = get_timeline_query(named_user)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def load_microblogging_mentions(request, name):
    """
    Use this function to get the timeline of mentions of the given user.
    """
    named_user = assert_active_user(name)
    query = get_mentions_query(named_user)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def load_microblogging_from_user(request, name):
    """
    Use this function to get the posts for the given user.
    """
    named_user = assert_active_user(name)
    query = get_microblogging_from_user_query(named_user)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def load_microblogging_for_followed_nodes(request, name):
    """
    Use this function to get a collection of blogposts regarding nodes
    which are followed by the user.
    """
    named_user = assert_active_user(name)
    query = get_microblogging_for_followed_nodes_query(named_user)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def load_microblogging_for_authored_nodes(request, name):
    """
    Use this function to get a collection of blogposts regarding nodes
    which are followed by the user.
    """
    named_user = assert_active_user(name)
    query = get_microblogging_for_authored_nodes_query(named_user)
    return microblogging_response(query, request.GET)


@ViewErrorHandling
def store_microblogging(request, path):
    assert_authentication(request)
    assert_post_parameters(request, ['microblogText'])
    post_text = convert_long_urls(request.POST['microblogText'],
                                  request.META['HTTP_HOST'])
    create_post(post_text, request.user, path)
    return json_response({'storeMicrobloggingResponse': {}})


############################## OLD STUFF #######################################
# Getter For Now only used for RSS

def get_mentions(username, count):
        users = User.objects.filter(username__iexact=username)
        named_user = users[0]
            
        feed_data = named_user.mentioning_entries.order_by('-time').distinct()
        feed_data = feed_data.prefetch_related('author', 'is_reference_to')[:count]
        return feed_data


def get_own(username, count):
        users = User.objects.filter(username__iexact=username)
        named_user = users[0]

        feed_data = Post.objects.filter(author=named_user).order_by('-time').distinct()
        feed_data = feed_data.prefetch_related('author', 'is_reference_to')[:count]
        return feed_data


def get_timeline(username, count):
        users = User.objects.filter(username__iexact=username)
        named_user = users[0]
        followed = Q(author__in=named_user.profile.followees.all())
        own = Q(author=named_user)
        feed_data = Post.objects.filter(followed | own).order_by('-time').distinct().prefetch_related('author', 'is_reference_to')[:20]
        return feed_data


def get_news():
        feed_data = Post.objects.order_by('-time')
        feed_data = feed_data.prefetch_related('author', 'is_reference_to')[:20]
        return feed_data


def get_newsAuthor(username, count):
        users = User.objects.filter(username__iexact=username)
        named_user = users[0]
        feed_data = Post.objects.filter(node_references__votes__user=named_user).order_by('-time')
        feed_data = feed_data.filter(node_references__text__authors=named_user)
        feed_data = feed_data.prefetch_related('author', 'is_reference_to')[:20]
        return feed_data


def get_newsFollow(username, count):
        users = User.objects.filter(username__iexact=username)
        named_user = users[0]
        feed_data = Post.objects.filter(node_references__votes__user=named_user).order_by('-time')
        feed_data = feed_data.prefetch_related('author', 'is_reference_to')[:20]
        return feed_data