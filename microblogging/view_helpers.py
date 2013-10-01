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
import json
from time import mktime
from django.db.models import Q
from findeco.error_handling import InvalidMicrobloggingOptions
from findeco.view_helpers import json_response
from .models import Post


def convert_response_list(post_list):
    response_list = []
    for post in post_list:
        authors = [post.author.username]
        if post.is_answer_to:
            authors.append(post.is_reference_to.author.username)
        response_list.append(
            {'microblogText': post.text_cache,
             'authorGroup': authors,
             'microblogTime': int(mktime(post.time.timetuple())),
             'microblogID': post.pk})
    return response_list


def convert_long_urls(request):
    """
    This function removes the unnecessary part from urls which are copy&pasted
    from the url field of the browser.
    """
    hostname = request.META['HTTP_HOST']
    text = request.POST['microblogText']
    text = text.replace("https://" + hostname, "")
    text = text.replace("http://" + hostname, "")
    text = text.replace(hostname, "")
    return text


def get_load_type(options):
    if "type" in options or 'id' in options:
        if not ('type' in options and 'id' in options):
            raise InvalidMicrobloggingOptions(json.dumps(options))

        if options["type"] not in ["newer", "older"]:
            raise InvalidMicrobloggingOptions(json.dumps(options))

        return options["type"], options["id"]

    else:
        return "newer", -1


def get_posts(query, options):
    load_type, load_id = get_load_type(options)
    posts = Post.objects.filter(query).distinct()
    if load_id == -1:
        return posts.order_by('-id')[:20]
    else:
        if load_type == "newer":
            return reversed(posts.filter(id__gt=load_id).order_by('id')[:20])
        elif load_type == "older":
            return posts.filter(id__lt=load_id).order_by('-id')[:20]


def microblogging_response(query, options):
    posts = get_posts(query, options)
    return json_response({
        'loadMicrobloggingResponse': convert_response_list(posts)})


