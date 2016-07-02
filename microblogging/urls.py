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

from django.conf.urls import url
from findeco.api_validation import USERNAME
from findeco.paths import RESTRICTED_PATH
from findeco.api_validation import RSSKEY
from microblogging.feeds import MicrobloggingFeed
from microblogging.views import load_microblogging_all, load_microblogging_for_node, load_microblogging_timeline
from microblogging.views import load_microblogging_mentions, load_microblogging_from_user
from microblogging.views import load_microblogging_for_followed_nodes, load_microblogging_for_authored_nodes
from microblogging.views import store_microblogging

RSSTYPE = r'(?P<rsstype>(timeline)|(mention)|(news)|(newsAuthor)|(newsFollow))'

microblogging_patterns = [
    url(r'^\.loadMicrobloggingAll/$',
        load_microblogging_all,
        name='load_microblogging_all'),

    url(r'^\.loadMicrobloggingForNode/' + RESTRICTED_PATH + '$',
        load_microblogging_for_node,
        name='load_microblogging_for_node'),

    url(r'^\.loadMicrobloggingTimeline/' + USERNAME + '/$',
        load_microblogging_timeline,
        name='load_microblogging_timeline'),

    url(r'^\.loadMicrobloggingMentions/' + USERNAME + '/$',
        load_microblogging_mentions,
        name='load_microblogging_mentions'),

    url(r'^\.loadMicrobloggingFromUser/' + USERNAME + '/$',
        load_microblogging_from_user,
        name='load_microblogging_from_user'),

    url(r'^\.loadMicrobloggingForFollowedNodes/' + USERNAME + '/$',
        load_microblogging_for_followed_nodes,
        name='load_microblogging_for_followed_nodes'),

    url(r'^\.loadMicrobloggingForAuthoredNodes/' + USERNAME + '/$',
        load_microblogging_for_authored_nodes,
        name='load_microblogging_for_authored_nodes'),

    url(r'^\.storeMicroblogging/' + RESTRICTED_PATH + '$',
        store_microblogging,
        name='store_microblogging'),

    # RSS Feed
    url(r'^feeds/rss/' + RSSTYPE + '/' + USERNAME + '/' + RSSKEY + '$',
        MicrobloggingFeed()),
]
