#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
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
#endregion #####################################################################
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