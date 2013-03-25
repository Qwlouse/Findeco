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
from django.conf.urls import patterns, include, url
from django.contrib import admin
from findeco.api_validation import USERNAME

from findeco.paths import PATH, RESTRICTED_PATH, ID
from findeco.views import is_logged_in

admin.autodiscover()

GRAPH_TYPE = r'(?P<graph_data_type>(default)|(full)|(withSpam))'
BLOG_ID = r'(?P<select_id>' + ID + ')'
BLOG_LOAD_TYPE = r'(?P<microblogging_load_type>(newer)|(older))'

urlpatterns = patterns(
    '',
    url(r'^' + PATH + '$', 'findeco.views.home', name='home'),

    url(r'^\.json_isLoggedIn/?$', "findeco.views.is_logged_in", name='is_logged_in'),

    url(r'^\.json_loadUserSettings/?$',
        'findeco.views.load_user_settings',
        name='load_user_settings'),

    url(r'^\.json_loadGraphData/' + GRAPH_TYPE + '/' + PATH + '$',
        'findeco.views.load_graph_data',
        name='load_graph_data'),

    url(r'^\.json_loadIndex/' + RESTRICTED_PATH + '$',
        'findeco.views.load_index',
        name='load_index'),

    url(r'^\.json_loadArgumentIndex/' + RESTRICTED_PATH + '$',
        'findeco.views.load_argument_index',
        name='load_argument_index'),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        RESTRICTED_PATH + '$',
        'microblogging.views.load_microblogging',
        name='load_microblogging'),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/' +
        RESTRICTED_PATH + '$',
        'microblogging.views.load_microblogging',
        name='load_microblogging',
        kwargs={'select_id': None}),

    url(r'^\.json_loadMicroblogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' +
        USERNAME + '$',
        'microblogging.views.load_timeline',
        name='load_timeline'),

    url(r'^\.json_loadMicroblogging/' + BLOG_LOAD_TYPE + '/' + USERNAME + '$',
        'microblogging.views.load_timeline',
        name='load_timeline',
        kwargs={'select_id': None}),

    url(r'^\.json_loadText/' + PATH + '$',
        'findeco.views.load_text',
        name='load_text'),

    url(r'^\.json_loadUserInfo/' + USERNAME + '/?$',
        'findeco.views.load_user_info',
        name='load_user_info'),

    url(r'^\.json_login/?$',
        'findeco.views.login',
        name='login'),

    url(r'^\.json_logout/?$',
        'findeco.views.logout',
        name='logout'),

    url(r'^\.json_markNode/follow/' + PATH + '$',
        'findeco.views.mark_node_follow',
        name='mark_node_follow'),

    url(r'^\.json_markNode/unfollow/' + PATH + '$',
        'findeco.views.mark_node_unfollow',
        name='mark_node_unfollow'),

    url(r'^\.json_markNode/spam/' + PATH + '$',
        'findeco.views.flag_node',
        name='flag_node'),

    url(r'^\.json_markNode/notspam/' + PATH + '$',
        'findeco.views.unflag_node',
        name='unflag_node'),

    url(r'^\.json_markUser/follow/' + USERNAME + '$',
        'findeco.views.mark_user_follow',
        name = 'mark_user_follow'),

    url(r'^\.json_markUser/unfollow/' + USERNAME + '$',
        'findeco.views.mark_user_unfollow',
        name = 'mark_user_unfollow'),

    url(r'^\.json_storeMicroblogPost/' + PATH + '$',
        'microblogging.views.store_microblog_post',
        name='store_microblog_post'),

    url(r'^\.json_storeSettings/?$',
        'findeco.views.store_settings',
        name='store_settings'),

    url(r'^\.json_storeText/' + PATH + '$',
        'findeco.views.store_text',
        name='store_text'),
                       
    url(r'^\.json_accountRegistration/?$',
        'findeco.views.account_registration',
        name='account_registration'),
                       
    url(r'^\.json_accountActivation/?$',
        'findeco.views.account_activation',
        name='account_activation'),
                       
    url(r'^\.json_accountResetRequestByMail/?$',
        'findeco.views.account_reset_request_by_mail',
        name='account_reset_request_by_mail'),

    url(r'^\.json_accountResetRequestByName/?$',
        'findeco.views.account_reset_request_by_name',
        name='account_reset_request_by_name'),
    
    url(r'^\.json_accountResetConfirmation/?$',
        'findeco.views.account_reset_confirmation',
        name='account_reset_confirmation'),                       
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^\.admin/doc/?', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^\.admin/?', include(admin.site.urls)),
)

handler404 = 'findeco.views.error_404'
