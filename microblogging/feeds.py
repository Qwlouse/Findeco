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

import hashlib

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.db.models import Q

from findeco.settings import FINDECO_BASE_URL
from findeco.view_helpers import assert_active_user
from microblogging.models import Post
from microblogging.view_helpers import (
    get_posts, get_timeline_query, get_mentions_query,
    get_microblogging_from_user_query,
    get_microblogging_for_followed_nodes_query)


def rsskey_is_valid(rsskey, name):
    user = User.objects.get(username=name)
    if rsskey == user.profile.api_key:
        return True
    else:
        return False


class MicrobloggingFeed(Feed):
    # item_guid_is_permalink = False

    def item_title(self, item):
        return item.author.username

    def item_link(self, item):
        return FINDECO_BASE_URL + "/" + item.location.get_a_path()

    def item_guid(self, item):
        return str(item.id)

    def item_date(self, item):
        return item.time

    def item_description(self, item):
        return item.text_cache

    def get_object(self, request, rsstype , rsskey , name):
        self.rsstype = rsstype

        if rsskey_is_valid(rsskey, name):
            self.link = FINDECO_BASE_URL + "/feeds/rss/timeline/" + name + "/rsskey/"
            self.feed_url = self.link
            self.feed_guid = hashlib.md5(self.link.encode('utf-8'))
            options = {}
            user = assert_active_user(name)
            if rsstype == "timeline":
                self.title = "Findeco - Timeline"
                self.description = "Deine Findeco Timeline"
                return get_posts(get_timeline_query(user), options)
            if rsstype == "mention":
                self.title = "Findeco - Mentions"
                self.description = "Posts in denen @%s erwähnt wird." % name
                return get_posts(get_mentions_query(user), options)
            if rsstype == "news":
                self.title = "Findeco - News"
                self.description = "Deine Findeco News"
                return get_posts(Q(), options)
            if rsstype == "newsAuthor":
                self.title = "Findeco - Autor News"
                self.description = "Posts von @%s." % name
                return get_posts(get_microblogging_from_user_query(user),
                                 options)
            if rsstype == "newsFollow":
                self.title = "Findeco - Folge News"
                self.description = "News zu Vorschlägen denen @%s folgt." % name
                return get_posts(
                    get_microblogging_for_followed_nodes_query(user), options)

        else:
            err = Post()
            err.title = "Non Matching Path"
            err.author.username = "System"
            return [err]

    def items(self, obj):
        return obj
