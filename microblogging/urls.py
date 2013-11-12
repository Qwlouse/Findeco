#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals
from django.conf.urls import patterns, url
from findeco.api_validation import USERNAME
from findeco.paths import RESTRICTED_PATH
from findeco.api_validation import RSSKEY
from .feeds import MicrobloggingFeed

RSSTYPE = r'(?P<rsstype>(timeline)|(mention)|(news)|(newsAuthor)|(newsFollow))'

microblogging_patterns = patterns('microblogging.views',
    url(r'^\.loadMicrobloggingAll/$',
        'load_microblogging_all',
        name='load_microblogging_all'),

    url(r'^\.loadMicrobloggingForNode/' + RESTRICTED_PATH + '$',
        'load_microblogging_for_node',
        name='load_microblogging_for_node'),

    url(r'^\.loadMicrobloggingTimeline/' + USERNAME + '/$',
        'load_microblogging_timeline',
        name='load_microblogging_timeline'),

    url(r'^\.loadMicrobloggingMentions/' + USERNAME + '/$',
        'load_microblogging_mentions',
        name='load_microblogging_mentions'),

    url(r'^\.loadMicrobloggingFromUser/' + USERNAME + '/$',
        'load_microblogging_from_user',
        name='load_microblogging_from_user'),

    url(r'^\.loadMicrobloggingForFollowedNodes/' + USERNAME + '/$',
        'load_microblogging_for_followed_nodes',
        name='load_microblogging_for_followed_nodes'),

    url(r'^\.loadMicrobloggingForAuthoredNodes/' + USERNAME + '/$',
        'load_microblogging_for_authored_nodes',
        name='load_microblogging_for_authored_nodes'),

    url(r'^\.storeMicroblogging/' + RESTRICTED_PATH + '$',
        'store_microblogging',
        name='store_microblogging'),

    # RSS Feed
    url(r'^feeds/rss/' + RSSTYPE + '/' + USERNAME + '/' + RSSKEY + '$',
        MicrobloggingFeed()),
)