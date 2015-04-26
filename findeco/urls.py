#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
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
# #############################################################################
#
# #############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################
from findeco import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from findeco.api_validation import USERNAME
from findeco.paths import PATH, UNNAMED_PATH, RESTRICTED_PATH
from microblogging.urls import microblogging_patterns

admin.autodiscover()

GRAPH_TYPE = r'(?P<graph_data_type>(default)|(full)|(withSpam))'
SEARCH_FIELDS = r'(?P<search_fields>((user|content|microblogging)' \
                r'(_(user|content|microblogging))*))'


# ########## Findeco API Calls ###########
urlpatterns = patterns(
    'findeco.views',

    # ----- User  -----
    url(r'^\.login/?$',
        'login',
        name='login'),

    url(r'^\.logout/?$',
        'logout',
        name='logout'),

    url(r'^\.loadUserSettings/?$',
        'load_user_settings',
        name='load_user_settings'),

    url(r'^\.storeSettings/?$',
        'store_settings',
        name='store_settings'),

    url(r'^\.accountRegistration/?$',
        'account_registration',
        name='account_registration'),

    url(r'^\.accountActivation/?$',
        'account_activation',
        name='account_activation'),

    url(r'^\.accountResetRequestByMail/?$',
        'account_reset_request_by_mail',
        name='account_reset_request_by_mail'),

    url(r'^\.accountResetRequestByName/?$',
        'account_reset_request_by_name',
        name='account_reset_request_by_name'),

    url(r'^\.accountResetConfirmation/?$',
        'account_reset_confirmation',
        name='account_reset_confirmation'),

    url(r'^\.emailChangeConfirmation/?$',
        'email_change_confirmation',
        name='email_change_confirmation'),

    url(r'^\.changePassword/?$',
        'change_password',
        name='change_password'),

    url(r'^\.deleteUser/?$',
        'delete_user',
        name='delete_user'),

    # ----- Interact with other users  -----
    url(r'^\.loadUserInfo/' + USERNAME + '/?$',
        'load_user_info',
        name='load_user_info'),

    url(r'^\.markUser/follow/' + USERNAME + '$',
        'mark_user_follow',
        name='mark_user_follow'),

    url(r'^\.markUser/unfollow/' + USERNAME + '$',
        'mark_user_unfollow',
        name='mark_user_unfollow'),

    # ----- Load Nodes  -----
    url(r'^\.loadNode/' + RESTRICTED_PATH + '$',
        'load_node',
        name='load_node'),

    url(r'^\.loadIndex/' + RESTRICTED_PATH + '$',
        'load_index',
        name='load_index'),

    url(r'^\.loadGraphData/' + GRAPH_TYPE + '/' + PATH + '$',
        'load_graph_data',
        name='load_graph_data'),

    url(r'^\.loadText/' + PATH + '$',
        'load_text',
        name='load_text'),

    url(r'^\.loadArgumentNews/?$',
        'load_argument_news',
        name='load_argument_news'),

    url(r'^\.loadArgumentIndex/' + RESTRICTED_PATH + '$',
        'load_argument_index',
        name='load_argument_index'),

    # ----- Mark Nodes  -----
    url(r'^\.markNode/follow/' + PATH + '$',
        'mark_node_follow',
        name='mark_node_follow'),

    url(r'^\.markNode/unfollow/' + PATH + '$',
        'mark_node_unfollow',
        name='mark_node_unfollow'),

    url(r'^\.markNode/spam/' + PATH + '$',
        'flag_node',
        name='flag_node'),

    url(r'^\.markNode/notspam/' + PATH + '$',
        'unflag_node',
        name='unflag_node'),

    # ----- Store Nodes  -----
    url(r'^\.storeProposal/' + PATH + '$',
        'store_proposal',
        name='store_proposal'),

    url(r'^\.storeRefinement/' + PATH + '$',
        'store_refinement',
        name='store_refinement'),

    url(r'^\.storeArgument/' + PATH + '$',
        'store_argument',
        name='store_argument'),

    # ----- Search  -----
    url(r'^\.search/'+SEARCH_FIELDS+'/(?P<search_string>(.*))$',
        'search',
        name='search')
)


# ########## Frontend Testing URLs ###########
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^.jasmine$', 'findeco.views.jasmine',
            name='jasmine_test_runner')
    )

# ########## Microblogging API ###########
urlpatterns += microblogging_patterns

# ########## Other urls ###########
urlpatterns += patterns(
    '',

    # admin docs
    url(r'^\.admin/doc/?', include('django.contrib.admindocs.urls')),

    # admin interface
    url(r'^\.admin/?', include(admin.site.urls)),

    url(r'^' + UNNAMED_PATH + '$', 'findeco.views.home', name='home'),

    url(r'^[^.].*', 'findeco.views.home', name='home'),
)


handler404 = 'findeco.views.error_404'
