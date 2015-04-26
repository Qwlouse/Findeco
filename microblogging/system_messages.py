#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>,
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
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from findeco.models import get_system_user
from microblogging.models import Post
from microblogging.view_helpers import notify_derivate, notify_new_argument
import node_storage


def post_node_was_flagged_message(path, user):
    post = Post()
    post.location = node_storage.get_node_for_path(path)
    post.author = get_system_user()
    post.post_type = Post.SPAM_MARKED
    post.save()
    post.mentions = [user]
    post.node_references = [post.location]
    post.render()
    return post


def post_node_was_unflagged_message(path, user):
    post = Post()
    post.location = node_storage.get_node_for_path(path)
    post.author = get_system_user()
    post.post_type = Post.SPAM_UNMARKED
    post.save()
    post.mentions = [user]
    post.node_references = [post.location]
    post.render()
    return post


def post_new_derivate_for_node_message(user, original_path, derivate_path):
    post = Post()

    original_node = node_storage.get_node_for_path(original_path)
    derivate_node = node_storage.get_node_for_path(derivate_path)

    post.location = original_node
    post.post_type = Post.NODE_REFINED
    post.author = get_system_user()
    post.save()
    post.node_references = [original_node, derivate_node]
    post.mentions = [user]
    post.render()

    # email notification
    notify_derivate(original_node, post)
    return post


def post_new_derivate_for_node_message_list(user, path_couples):
    posts = []
    for old_path, new_path in path_couples:
        posts.append(post_new_derivate_for_node_message(user, old_path,
                                                        new_path))
    return posts


def post_new_argument_for_node_message(user, path, arg_type, arg_path):
    post = Post()
    post.location = node_storage.get_node_for_path(path)
    post.author = get_system_user()
    post.post_type = Post.ARGUMENT_CREATED
    post.save()
    post.mentions = [user]
    post.node_references = [node_storage.get_node_for_path(arg_path),
                            post.location]
    post.render()

    # email notification
    notify_new_argument(post.location, post)
    return post
