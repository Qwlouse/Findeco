#!/usr/bin/python
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
from __future__ import division, print_function, unicode_literals
from django.core.urlresolvers import resolve, Resolver404
from django.test import TestCase

from ..views import (load_user_settings, load_index, load_graph_data,
                     load_text, load_user_info, load_argument_index, login,
                     logout, flag_node, unflag_node, store_text,
                     mark_node_follow, mark_node_unfollow, store_settings,
                     store_proposal, store_refinement)


# ########################## Test the API calls ###############################
valid_routes = [
    # ### loadGraphData
    dict(url='/.loadGraphData/default/some.1/path.2',
         func=load_graph_data,
         url_name='load_graph_data',
         kwargs=dict(graph_data_type='default', path='some.1/path.2')),

    dict(url='/.loadGraphData/full/some.1/path.2',
         func=load_graph_data,
         url_name='load_graph_data',
         kwargs=dict(graph_data_type='full', path='some.1/path.2')),

    dict(url='/.loadGraphData/withSpam/some.1/path.2',
         func=load_graph_data,
         url_name='load_graph_data',
         kwargs=dict(graph_data_type='withSpam', path='some.1/path.2')),

    # ### loadIndex
    dict(url='/.loadIndex/some.1/path.2',
         func=load_index,
         url_name='load_index',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.loadArgumentIndex/some.1/path.2',
         func=load_argument_index,
         url_name='load_argument_index',
         kwargs=dict(path='some.1/path.2')),

    # ### loadText
    dict(url='/.loadText/some.1/path.2',
         func=load_text,
         url_name='load_text',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.loadText/some.1/path',
         func=load_text,
         url_name='load_text',
         kwargs=dict(path='some.1/path')),

    dict(url='/.loadText/some.1/path.2.neut.17',
         func=load_text,
         url_name='load_text',
         kwargs=dict(path='some.1/path.2.neut.17')),

    dict(url='/.loadText/some.1/path.2.con.1/',
         func=load_text,
         url_name='load_text',
         kwargs=dict(path='some.1/path.2.con.1')),

    dict(url='/.loadText/some.1/path.2.pro.144',
         func=load_text,
         url_name='load_text',
         kwargs=dict(path='some.1/path.2.pro.144')),

    # ### loadUserInfo
    dict(url='/.loadUserInfo/somebody',
         func=load_user_info,
         url_name='load_user_info',
         kwargs=dict(name='somebody')),

    dict(url='/.loadUserInfo/somebody/',
         func=load_user_info,
         url_name='load_user_info',
         kwargs=dict(name='somebody')),

    # ### loadUserSettings
    dict(url='/.loadUserSettings/',
         func=load_user_settings,
         url_name='load_user_settings',
         kwargs=dict()),

    dict(url='/.loadUserSettings',
         func=load_user_settings,
         url_name='load_user_settings',
         kwargs=dict()),

    # ### login
    dict(url='/.login/',
         func=login,
         url_name='login',
         kwargs=dict()),

    # ### logout
    dict(url='/.logout/',
         func=logout,
         url_name='logout',
         kwargs=dict()),

    # ### markNode
    dict(url='/.markNode/spam/some.1/path.2',
         func=flag_node,
         url_name='flag_node',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.markNode/notspam/some.1/path.2',
         func=unflag_node,
         url_name='unflag_node',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.markNode/follow/some.1/path.2',
         func=mark_node_follow,
         url_name='mark_node_follow',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.markNode/unfollow/some.1/path.2',
         func=mark_node_unfollow,
         url_name='mark_node_unfollow',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.markNode/spam/some.1/path.2.pro.1',
         func=flag_node,
         url_name='flag_node',
         kwargs=dict(path='some.1/path.2.pro.1')),

    dict(url='/.markNode/notspam/some.1/path.2.pro.1',
         func=unflag_node,
         url_name='unflag_node',
         kwargs=dict(path='some.1/path.2.pro.1')),

    dict(url='/.markNode/follow/some.1/path.2.pro.1',
         func=mark_node_follow,
         url_name='mark_node_follow',
         kwargs=dict(path='some.1/path.2.pro.1')),

    dict(url='/.markNode/unfollow/some.1/path.2.pro.1',
         func=mark_node_unfollow,
         url_name='mark_node_unfollow',
         kwargs=dict(path='some.1/path.2.pro.1')),

    dict(url='/.markNode/spam/some.1/path.2.con.003',
         func=flag_node,
         url_name='flag_node',
         kwargs=dict(path='some.1/path.2.con.003')),

    dict(url='/.markNode/notspam/some.1/path.2.con.003',
         func=unflag_node,
         url_name='unflag_node',
         kwargs=dict(path='some.1/path.2.con.003')),

    dict(url='/.markNode/follow/some.1/path.2.con.003',
         func=mark_node_follow,
         url_name='mark_node_follow',
         kwargs=dict(path='some.1/path.2.con.003')),

    dict(url='/.markNode/unfollow/some.1/path.2.con.003',
         func=mark_node_unfollow,
         url_name='mark_node_unfollow',
         kwargs=dict(path='some.1/path.2.con.003')),

    dict(url='/.markNode/spam/some.1/path.2.neut.8437569384',
         func=flag_node,
         url_name='flag_node',
         kwargs=dict(path='some.1/path.2.neut.8437569384')),

    dict(url='/.markNode/notspam/some.1/path.2.neut.8437569384',
         func=unflag_node,
         url_name='unflag_node',
         kwargs=dict(path='some.1/path.2.neut.8437569384')),

    dict(url='/.markNode/follow/some.1/path.2.neut.8437569384',
         func=mark_node_follow,
         url_name='mark_node_follow',
         kwargs=dict(path='some.1/path.2.neut.8437569384')),

    dict(url='/.markNode/unfollow/some.1/path.2.neut.8437569384',
         func=mark_node_unfollow,
         url_name='mark_node_unfollow',
         kwargs=dict(path='some.1/path.2.neut.8437569384')),

    # ### storeSettings
    dict(url='/.storeSettings/',
         func=store_settings,
         url_name='store_settings',
         kwargs=dict()),

    # ### storeText
    dict(url='/.storeText/some.1/path.2',
         func=store_text,
         url_name='store_text',
         kwargs=dict(path='some.1/path.2')),

    dict(url='/.storeText/some.1/path.2.neut.5',
         func=store_text,
         url_name='store_text',
         kwargs=dict(path='some.1/path.2.neut.5')),

    dict(url='/.storeText/some.1/path.2.con.995',
         func=store_text,
         url_name='store_text',
         kwargs=dict(path='some.1/path.2.con.995')),

    dict(url='/.storeText/some.1/path.2.pro.1',
         func=store_text,
         url_name='store_text',
         kwargs=dict(path='some.1/path.2.pro.1')),

    # ### storeProposal
    dict(url='/.storeProposal/some.1/path.2',
         func=store_proposal,
         url_name='store_proposal',
         kwargs=dict(path='some.1/path.2')),

    # ### storeRefinement
    dict(url='/.storeRefinement/some.1/path.2',
         func=store_refinement,
         url_name='store_refinement',
         kwargs=dict(path='some.1/path.2')),
]

invalid_routes = [
    # ### loadGraphData
    dict(url='/.loadGraphData/defualt/some.1/path.2'),
    dict(url='/.loadGraphData/fuell/some.1/path.2'),
    dict(url='/.loadGraphData/witSpam/some.1/path.2'),
    # ### loadIndex
    dict(url='/.loadIndex/some.1\path.2'),
    dict(url='/.loadIndex/some.1/path.2.proo'),
    dict(url='/.loadIndex/some.1/path.2.newt'),
    dict(url='/.loadIndex/some.1/path.2.bon'),
    dict(url='/.loadIndex/some.1/path.2.ill'),
    # ### loadText
    dict(url='/.loadText/1.some/path.2'),
    dict(url='/.loadText/some.1/2.path'),
    dict(url='/.loadText/some.1/path.2.17'),
    dict(url='/.loadText/some.1/path.2.conn.1/'),
    dict(url='/.loadText/some.1/path.2.pro.name.144'),
    # ### loadUserInfo
    dict(url='/.loadUserInfo/somebody/some.1/path.2'),
    dict(url='/.loadUserInfo/'),
    # ### loadUserSettings
    dict(url='/.loadUserSettings/some.1/path.2'),
    dict(url='/.loadUserSettings/username'),
    # ### login
    dict(url='/.login/some.1/path.2'),
    # ### logout
    dict(url='/.logout/some.1/path.2'),
    # ### markNode
    dict(url='/.markNode/spamm/some.1/path.2'),
    dict(url='/.markNode/nospam/some.1/path.2'),
    dict(url='/.markNode/follows/some.1/path.2'),
    dict(url='/.markNode/unfollows/some.1/path.2'),
    dict(url='/.markNode/some.1/path.2.pro.1'),
    dict(url='/.markNode/some.1/path.2.pro.1'),
    dict(url='/.markNode/123/some.1/path.2.pro.1'),
    dict(url='/.markNode/unspam/some.1/path.2.pro.1'),
    dict(url='/.markNode/003/some.1/path.2.con.003'),
    dict(url='/.markNode/notspam/some.1/path.2.conn.003'),
    dict(url='/.markNode/follow/some.1/path.2.con.name.003'),
    dict(url='/.markNode/unfollow/1/path.2.con.003'),
    dict(url='/.markNode/spam/some.1/path.2.newt.8437569384'),
    dict(url='/.markNode/notspam/some.1/path.2.8437569384'),
    dict(url='/.markNode/follow/some.1/path.2.neut.name.8437569384'),
    dict(url='/.markNode/unfollow/some.1/path.2.num.8437569384'),
    # ### storeSettings
    dict(url='/.storeSettings/some.1/path.2'),
    # ### storeText
    dict(url='/.storeText/some.1/path.2.5'),
    dict(url='/.storeText/bla/some.1/path.2.neut.5'),
    dict(url='/.storeText/some.1/path.2.con.995.77'),
    dict(url='/.storeText/some.1/path.2.prow.1')
]


class UrlResolutionTest(TestCase):
    def test_routing(self):
        for route in valid_routes:
            try:
                res = resolve(route['url'])
            except Resolver404:
                self.fail("Could not resolve: '%s'" % route['url'])
            self.assertEqual(res.url_name, route['url_name'])
            self.assertEqual(res.func, route['func'])
            if 'kwargs' in route:
                self.assertEqual(res.kwargs, route['kwargs'])

    def test_routing_fail(self):
        for route in invalid_routes:
            try:
                res = resolve(route['url'])
                self.fail("Resolved invalid url: '%s' as %s" % (
                    route['url'], res.url_name))
            except Resolver404:
                pass
