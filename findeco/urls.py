#!/usr/bin/python
# coding=utf-8
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
################################################################################
from libs import django_cron
from django.conf.urls import patterns, include, url
from django.contrib import admin
from findeco.api_validation import USERNAME, RSSKEY
from findeco.feeds import RssFeed, AtomFeed
from findeco.paths import PATH, RESTRICTED_PATH, ID

admin.autodiscover()
django_cron.autodiscover()


GRAPH_TYPE = r'(?P<graph_data_type>(default)|(full)|(withSpam))'
BLOG_ID = r'(?P<select_id>' + ID + ')'
BLOG_LOAD_TYPE = r'(?P<microblogging_load_type>(newer)|(older))'
SEARCH_FIELDS = r'(?P<search_fields>((user|content|microblogging)' \
                r'(_(user|content|microblogging))*))'
RSSTYPE = r'(?P<rsstype>(timeline)|(mention)|(news)|(newsAuthor)|(newsFollow))'


########### Findeco API Calls ###########
urlpatterns = patterns(
    'findeco.views',

    # ----- User  -----
    url(r'^\.json_login/?$',
        'login',
        name='login'),

    url(r'^\.json_logout/?$',
        'logout',
        name='logout'),

    url(r'^\.json_loadUserSettings/?$',
        'load_user_settings',
        name='load_user_settings'),

    url(r'^\.json_storeSettings/?$',
        'store_settings',
        name='store_settings'),

    url(r'^\.json_accountRegistration/?$',
        'account_registration',
        name='account_registration'),

    url(r'^\.json_accountActivation/?$',
        'account_activation',
        name='account_activation'),

    url(r'^\.json_accountResetRequestByMail/?$',
        'account_reset_request_by_mail',
        name='account_reset_request_by_mail'),

    url(r'^\.json_accountResetRequestByName/?$',
        'account_reset_request_by_name',
        name='account_reset_request_by_name'),

    url(r'^\.json_accountResetConfirmation/?$',
        'account_reset_confirmation',
        name='account_reset_confirmation'),

    url(r'^\.json_emailChangeConfirmation/?$',
        'email_change_confirmation',
        name='email_change_confirmation'),

    url(r'^\.json_changePassword/?$',
        'change_password',
        name='change_password'),

    url(r'^\.json_deleteUser/?$',
        'delete_user',
        name='delete_user'),

    # ----- Interact with other users  -----
    url(r'^\.json_loadUserInfo/' + USERNAME + '/?$',
        'load_user_info',
        name='load_user_info'),

    url(r'^\.json_markUser/follow/' + USERNAME + '$',
        'mark_user_follow',
        name='mark_user_follow'),

    url(r'^\.json_markUser/unfollow/' + USERNAME + '$',
        'mark_user_unfollow',
        name='mark_user_unfollow'),

    # ----- Load Nodes  -----
    url(r'^\.json_loadNode/' + RESTRICTED_PATH + '$',
        'load_node',
        name='load_node'),

    url(r'^\.json_loadIndex/' + RESTRICTED_PATH + '$',
        'load_index',
        name='load_index'),

    url(r'^\.json_loadGraphData/' + GRAPH_TYPE + '/' + PATH + '$',
        'load_graph_data',
        name='load_graph_data'),

    url(r'^\.json_loadText/' + PATH + '$',
        'load_text',
        name='load_text'),

    url(r'^\.json_loadArgumentIndex/' + RESTRICTED_PATH + '$',
        'load_argument_index',
        name='load_argument_index'),

    # ----- Mark Nodes  -----
    url(r'^\.json_markNode/follow/' + PATH + '$',
        'mark_node_follow',
        name='mark_node_follow'),

    url(r'^\.json_markNode/unfollow/' + PATH + '$',
        'mark_node_unfollow',
        name='mark_node_unfollow'),

    url(r'^\.json_markNode/spam/' + PATH + '$',
        'flag_node',
        name='flag_node'),

    url(r'^\.json_markNode/notspam/' + PATH + '$',
        'unflag_node',
        name='unflag_node'),

    # ----- Store Nodes  -----
    url(r'^\.json_storeText/' + PATH + '$',
        'store_text',
        name='store_text'),

    # ----- Search  -----
    url(r'^\.json_search/'+SEARCH_FIELDS+'/(?P<search_string>(.*))$',
        'search',
        name='search')
)

########### Microblogging API ###########
urlpatterns += patterns(
    'microblogging.views',

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        RESTRICTED_PATH + '$',
        'load_microblogging',
        name='load_microblogging'),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/' +
        RESTRICTED_PATH + '$',
        'load_microblogging',
        name='load_microblogging',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        USERNAME + '$',
        'load_timeline',
        name='load_timeline'),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/' + USERNAME + '$',
        'load_timeline',
        name='load_timeline',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/mentions/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        USERNAME + '$',
        'load_mentions',
        name='load_mentions'),

    url(r'^\.json_loadMicroblogging/mentions/' + BLOG_LOAD_TYPE + '/' + USERNAME + '$',
        'load_mentions',
        name='load_mentions',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/own/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        USERNAME + '$',
        'load_own',
        name='load_own'),

    url(r'^\.json_loadMicroblogging/own/' + BLOG_LOAD_TYPE + '/' + USERNAME + '$',
        'load_own',
        name='load_own',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/:collection$',
        'load_collection',
        name='load_collection'),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/:collection$',
        'load_collection',
        name='load_collection',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/:collectionAuthor$',
        'load_collection',
        name='load_collection_author',
        kwargs={'only_author': True}),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/:collectionAuthor$',
        'load_collection',
        name='load_collection_author',
        kwargs={'select_id': None, 'only_author': True}),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/:collectionAll$',
        'load_collection',
        name='load_collection_all',
        kwargs={'all_nodes': True}),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/:collectionAll$',
        'load_collection',
        name='load_collection_all',
        kwargs={'select_id': None, 'all_nodes': True}),

    url(r'^\.json_storeMicroblogPost/' + PATH + '$',
        'store_microblog_post',
        name='store_microblog_post'),
)

########### Other urls ###########
urlpatterns += patterns(
    '',

    # RSS Feed
    url(r'^feeds/rss/' + RSSTYPE + '/' + USERNAME + '/' + RSSKEY + '$', RssFeed()),

    # admin docs
    url(r'^\.admin/doc/?', include('django.contrib.admindocs.urls')),

    # admin interface
    url(r'^\.admin/?', include(admin.site.urls)),

    url(r'^' + PATH + '$', 'findeco.views.home', name='home'),

    url(r'.*', 'findeco.views.home', name='home', kwargs={'path': 'wildcard'}),
)


handler404 = 'findeco.views.error_404'
