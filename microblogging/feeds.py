#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
import hashlib

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.db.models import Q

from findeco.settings import FINDECO_BASE_URL
from findeco.view_helpers import assert_active_user
from microblogging.models import Post
from microblogging.view_helpers import *


def rsskey_is_valid(rsskey, name):
    user = User.objects.get(username=name)
    if rsskey == user.profile.api_key:
        return True
    else:
        return False


class MicrobloggingFeed(Feed):
    #item_guid_is_permalink = False

    def item_title(self, item):
        return item.author.username

    def item_link(self, item):
        return "/" + item.location.get_a_path()

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
            self.feed_guid = hashlib.md5(self.link)
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

