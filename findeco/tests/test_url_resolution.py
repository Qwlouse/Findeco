#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
from django.core.urlresolvers import resolve, Resolver404

from django.test import TestCase

from ..views import load_user_settings, load_index, load_graph_data, load_text
from ..views import load_user_info, load_argument_index
from ..views import login, logout, mark_node, store_settings, store_text
from microblogging.views import load_microblogging, store_microblog_post

########################### Test the API calls #################################
valid_routes = [
    #### loadGraphData
    dict(url='/.json_loadGraphData/default/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='default', path='some.1/path.2')),

    dict(url='/.json_loadGraphData/full/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='full', path='some.1/path.2')),

    dict(url='/.json_loadGraphData/withSpam/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='withSpam', path='some.1/path.2')),

    #### loadIndex
    dict(url='/.json_loadIndex/some.1/path.2',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='some.1/path.2')),

    dict(url='/.json_loadIndex/False/some.1/path.2',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='some.1/path.2')),

    dict(url='/.json_loadIndex/True/some.1/path.2',
        func=load_argument_index,
        url_name='load_argument_index',
        kwargs=dict(path='some.1/path.2')),

    #### loadMicroBlogging
    dict(url='/.json_loadMicroBlogging/0/newer/some.1/path.2',
        func=load_microblogging,
        url_name='load_microblogging',
        kwargs=dict(path='some.1/path.2', select_id='0', microblogging_load_type='newer')),

    dict(url='/.json_loadMicroBlogging/74/newer/some.1/path.2',
        func=load_microblogging,
        url_name='load_microblogging',
        kwargs=dict(path='some.1/path.2', select_id='74', microblogging_load_type='newer')),

    dict(url='/.json_loadMicroBlogging/0/older/some.1/path.2',
        func=load_microblogging,
        url_name='load_microblogging',
        kwargs=dict(path='some.1/path.2', select_id='0', microblogging_load_type='older')),

    dict(url='/.json_loadMicroBlogging/74/older/some.1/path.2',
        func=load_microblogging,
        url_name='load_microblogging',
        kwargs=dict(path='some.1/path.2', select_id='74', microblogging_load_type='older')),

    dict(url='/.json_loadMicroBlogging/74/older/some.1/path.2',
        func=load_microblogging,
        url_name='load_microblogging',
        kwargs=dict(path='some.1/path.2', select_id=None, microblogging_load_type='older')),

    #### loadText
    dict(url='/.json_loadText/some.1/path.2',
        func=load_text,
        url_name='load_text',
        kwargs=dict(path='some.1/path.2')),

    dict(url='/.json_loadText/some.1/path',
        func=load_text,
        url_name='load_text',
        kwargs=dict(path='some.1/path')),

    dict(url='/.json_loadText/some.1/path.2.neut.17',
        func=load_text,
        url_name='load_text',
        kwargs=dict(path='some.1/path.2.neut.17')),

    dict(url='/.json_loadText/some.1/path.2.con.1/',
        func=load_text,
        url_name='load_text',
        kwargs=dict(path='some.1/path.2.con.1')),

    dict(url='/.json_loadText/some.1/path.2.pro.144',
        func=load_text,
        url_name='load_text',
        kwargs=dict(path='some.1/path.2.pro.144')),

    #### loadUserInfo
    dict(url='/.json_loadUserInfo/somebody',
        func=load_user_info,
        url_name='load_user_info',
        kwargs=dict(name='somebody')),

    dict(url='/.json_loadUserInfo/somebody/',
        func=load_user_info,
        url_name='load_user_info',
        kwargs=dict(name='somebody')),

    #### loadUserSettings
    dict(url='/.json_loadUserSettings/',
        func=load_user_settings,
        url_name='load_user_settings',
        kwargs=dict()),

    dict(url='/.json_loadUserSettings',
        func=load_user_settings,
        url_name='load_user_settings',
        kwargs=dict()),

    #### login
    dict(url='/.json_login/',
        func=login,
        url_name='login',
        kwargs=dict()),

    #### logout
    dict(url='/.json_logout/',
        func=logout,
        url_name='logout',
        kwargs=dict()),

    #### markNode
    dict(url='/.json_markNode/spam/some.1/path.2',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2', mark_type='spam')),

    dict(url='/.json_markNode/notspam/some.1/path.2',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2', mark_type='notspam')),

    dict(url='/.json_markNode/follow/some.1/path.2',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2', mark_type='follow')),

    dict(url='/.json_markNode/unfollow/some.1/path.2',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2', mark_type='unfollow')),

    dict(url='/.json_markNode/spam/some.1/path.2.pro.1',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.pro.1', mark_type='spam')),

    dict(url='/.json_markNode/notspam/some.1/path.2.pro.1',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.pro.1', mark_type='notspam')),

    dict(url='/.json_markNode/follow/some.1/path.2.pro.1',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.pro.1', mark_type='follow')),

    dict(url='/.json_markNode/unfollow/some.1/path.2.pro.1',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.pro.1', mark_type='unfollow')),

    dict(url='/.json_markNode/spam/some.1/path.2.con.003',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.con.003', mark_type='spam')),

    dict(url='/.json_markNode/notspam/some.1/path.2.con.003',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.con.003', mark_type='notspam')),

    dict(url='/.json_markNode/follow/some.1/path.2.con.003',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.con.003', mark_type='follow')),

    dict(url='/.json_markNode/unfollow/some.1/path.2.con.003',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.con.003', mark_type='unfollow')),

    dict(url='/.json_markNode/spam/some.1/path.2.neut.8437569384',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.neut.8437569384', mark_type='spam')),

    dict(url='/.json_markNode/notspam/some.1/path.2.neut.8437569384',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.neut.8437569384', mark_type='notspam')),

    dict(url='/.json_markNode/follow/some.1/path.2.neut.8437569384',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.neut.8437569384', mark_type='follow')),

    dict(url='/.json_markNode/unfollow/some.1/path.2.neut.8437569384',
        func=mark_node,
        url_name='mark_node',
        kwargs=dict(path='some.1/path.2.neut.8437569384', mark_type='unfollow')),

    #### storeMicroBlogPost
    dict(url='/.json_storeMicroBlogPost/some.1/path.2',
        func=store_microblog_post,
        url_name='store_microblog_post',
        kwargs=dict(path='some.1/path.2')),

    #### storeSettings
    dict(url='/.json_storeSettings/',
        func=store_settings,
        url_name='store_settings',
        kwargs=dict()),

    #### storeText
    dict(url='/.json_storeText/some.1/path.2',
        func=store_text,
        url_name='store_text',
        kwargs=dict(path='some.1/path.2')),

    dict(url='/.json_storeText/some.1/path.2.neut.5',
        func=store_text,
        url_name='store_text',
        kwargs=dict(path='some.1/path.2.neut.5')),

    dict(url='/.json_storeText/some.1/path.2.con.995',
        func=store_text,
        url_name='store_text',
        kwargs=dict(path='some.1/path.2.con.995')),

    dict(url='/.json_storeText/some.1/path.2.pro.1',
        func=store_text,
        url_name='store_text',
        kwargs=dict(path='some.1/path.2.pro.1')),
    ]

invalid_routes = [
    #### loadGraphData
    dict(url='/.json_loadGraphData/defualt/some.1/path.2'),
    dict(url='/.json_loadGraphData/fuell/some.1/path.2'),
    dict(url='/.json_loadGraphData/witSpam/some.1/path.2'),
    #### loadIndex
    dict(url='/.json_loadIndex/some.1\path.2'),
    dict(url='/.json_loadIndex/some.1/path.2.proo'),
    dict(url='/.json_loadIndex/some.1/path.2.newt'),
    dict(url='/.json_loadIndex/some.1/path.2.bon'),
    dict(url='/.json_loadIndex/some.1/path.2.ill'),
    #### loadMicroBlogging
    dict(url='/.json_loadMicroBlogging/-1/newer/some.1/path.2'),
    dict(url='/.json_loadMicroBlogging/74/newwer/some.1/path.2'),
    dict(url='/.json_loadMicroBlogging/older/12/some.1/path.2'),
    dict(url='/.json_loadMicroBlogging/74/older/newer/some.1/path.2'),
    #### loadText
    dict(url='/.json_loadText/1.some/path.2'),
    dict(url='/.json_loadText/some.1/2.path'),
    dict(url='/.json_loadText/some.1/path.2.17'),
    dict(url='/.json_loadText/some.1/path.2.conn.1/'),
    dict(url='/.json_loadText/some.1/path.2.pro.name.144'),
    #### loadUserInfo
    dict(url='/.json_loadUserInfo/somebody/some.1/path.2'),
    dict(url='/.json_loadUserInfo/'),
    #### loadUserSettings
    dict(url='/.json_loadUserSettings/some.1/path.2'),
    dict(url='/.json_loadUserSettings/username'),
    #### login
    dict(url='/.json_login/some.1/path.2'),
    #### logout
    dict(url='/.json_logout/some.1/path.2'),
    #### markNode
    dict(url='/.json_markNode/spamm/some.1/path.2'),
    dict(url='/.json_markNode/nospam/some.1/path.2'),
    dict(url='/.json_markNode/follows/some.1/path.2'),
    dict(url='/.json_markNode/unfollows/some.1/path.2'),
    dict(url='/.json_markNode/some.1/path.2.pro.1'),
    dict(url='/.json_markNode/some.1/path.2.pro.1'),
    dict(url='/.json_markNode/123/some.1/path.2.pro.1'),
    dict(url='/.json_markNode/unspam/some.1/path.2.pro.1'),
    dict(url='/.json_markNode/003/some.1/path.2.con.003'),
    dict(url='/.json_markNode/notspam/some.1/path.2.conn.003'),
    dict(url='/.json_markNode/follow/some.1/path.2.con.name.003'),
    dict(url='/.json_markNode/unfollow/1/path.2.con.003'),
    dict(url='/.json_markNode/spam/some.1/path.2.newt.8437569384'),
    dict(url='/.json_markNode/notspam/some.1/path.2.8437569384'),
    dict(url='/.json_markNode/follow/some.1/path.2.neut.name.8437569384'),
    dict(url='/.json_markNode/unfollow/some.1/path.2.num.8437569384'),
    #### storeMicroBlogPost
    dict(url='/.json_storeMicruBlogPost/'),
    #### storeSettings
    dict(url='/.json_storeSettings/some.1/path.2'),
    #### storeText
    dict(url='/.json_storeText/some.1/path.2.5'),
    dict(url='/.json_storeText/bla/some.1/path.2.neut.5'),
    dict(url='/.json_storeText/some.1/path.2.con.995.77'),
    dict(url='/.json_storeText/some.1/path.2.prow.1'),
    ]

class UrlResolutionTest(TestCase):
    def test_routing(self):
        for route in valid_routes:
            try:
                res = resolve(route['url'])
            except Resolver404:
                self.fail("Could not resolve: '%s'"%route['url'])
            self.assertEqual(res.url_name, route['url_name'])
            self.assertEqual(res.func, route['func'])
            if 'kwargs' in route:
                self.assertEqual(res.kwargs, route['kwargs'])

    def test_routing_fail(self):
        for route in invalid_routes:
            try:
                res = resolve(route['url'])
                self.fail("Resolved invalid url: '%s' as %s"%(route['url'],res.url_name))
            except Resolver404:
                pass
