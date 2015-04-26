#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>
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

from time import mktime
from findeco.search_tools import get_search_query
from microblogging.models import Post


def convert_to_response_list(post_list):
    response_list = []
    for post in post_list:
        authors = [post.author.username]
        if post.is_answer_to:
            authors.append(post.is_reference_to.author.username)
        response_list.append(
            {'microblogText': post.text_cache,
             'authorGroup': authors,
             'location': post.location_id,
             'locationPath': post.location.get_a_path(),
             'microblogTime': int(mktime(post.time.timetuple())),
             'microblogID': post.pk})
    return response_list


def search_for_microblogging(search_string):
    microblogging_query = get_search_query(search_string, ['text_cache', ])
    found_posts = Post.objects.filter(microblogging_query).order_by("-id")
    return convert_to_response_list(found_posts)


def change_microblogging_authorship(old_user, new_user):
    # change author of post to new user
    for post in old_user.microblogging_posts.all():
        post.author = new_user
        post.render()
        post.save()

    # change mention of post to new user
    for post in Post.objects.filter(mentions=old_user):
        old_order = [u.id for u in post.mentions.order_by('id')]
        post.mentions.remove(old_user)
        post.mentions.add(new_user)
        post.save()
        new_order = [u.id for u in post.mentions.order_by('id')]

        permutation = []
        for user_id in old_order:
            if user_id == old_user.id:
                permutation.append(new_order.index(new_user.id))
            else:
                permutation.append(new_order.index(user_id))

        for i in range(len(permutation)):
            post.text_template = post.text_template.replace('{u%d}' % i,
                                                            '{P%d}' % i)

        for i, p in enumerate(permutation):
            post.text_template = post.text_template.replace('{P%d}' % i,
                                                            '{u%d}' % p)
        post.render()


def delete_posts_referring_to(node):
    Post.objects.filter(node_references=node).delete()
    Post.objects.filter(location=node).delete()
