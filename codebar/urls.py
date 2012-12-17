#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from codebar.paths import PATH, ID

GRAPH_TYPE = r'(?P<graph_data_type>(default)|(full)|(withSpam))'
BLOG_ID = r'(?P<select_id>' + ID + ')'
BLOG_LOAD_TYPE = r'(?P<microblogging_load_type>(newer)|(older))'
USERNAME = r'(?P<name>[a-zA-Z][a-zA-Z0-9-_]{0,19})'
MARK_TYPE = r'(?P<mark_type>(spam)|(notspam)|(follow)|(unfollow))'


urlpatterns = patterns('',
    url(r'^$', 'codebar.views.home', name='home'),

    url(r'^\.json_loadUserSettings/?$',
        'codebar.views.load_user_settings',
        name='load_user_settings'),

    url(r'^\.json_loadGraphData/' + GRAPH_TYPE + '/' + PATH + '$',
        'codebar.views.load_graph_data',
        name='load_graph_data'),

    url(r'^\.json_loadIndex/' + PATH + '$',
        'codebar.views.load_index',
        name='load_index'),

    url(r'^\.json_loadMicroBlogging/' + BLOG_ID + '/' + BLOG_LOAD_TYPE + '/' + PATH + '$',
        'codebar.views.load_microblogging',
        name='load_microblogging'),

    url(r'^\.json_loadText/' + PATH + '$',
        'codebar.views.load_text',
        name='load_text'),

    url(r'^\.json_loadUserInfo/' + USERNAME + '/?$',
        'codebar.views.load_user_info',
        name='load_user_info'),

    url(r'^\.json_login/?$',
        'codebar.views.login',
        name='login'),

    url(r'^\.json_logout/?$',
        'codebar.views.logout',
        name='logout'),

    url(r'^\.json_markNode/' + MARK_TYPE + '/' + PATH + '$',
        'codebar.views.mark_node',
        name='mark_node'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^\.admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^\.admin/', include(admin.site.urls)),
)
