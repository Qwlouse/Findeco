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
from __future__ import division, print_function, unicode_literals
from django.core.urlresolvers import resolve, Resolver404

import unittest

from ..views import load_user_settings, load_index, load_graph_data

########################### Test the API calls #################################
valid_routes = [
    #### loadUserSettings
    dict(url='/.json_loadUserSettings',
        func=load_user_settings,
        url_name='load_user_settings'),

    #### loadIndex
    dict(url='/.json_loadIndex/some.1/path.2',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='/some.1/path.2')),

    dict(url='/.json_loadIndex/some.1/path.2.pro',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='/some.1/path.2.pro')),

    dict(url='/.json_loadIndex/some.1/path.2.neut',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='/some.1/path.2.neut')),

    dict(url='/.json_loadIndex/some.1/path.2.con',
        func=load_index,
        url_name='load_index',
        kwargs=dict(path='/some.1/path.2.con')),

    #### loadGraphData
    dict(url='/.json_loadGraphData/default/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='default', path='/some.1/path.2')),

    dict(url='/.json_loadGraphData/full/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='full', path='/some.1/path.2')),

    dict(url='/.json_loadGraphData/withSpam/some.1/path.2',
        func=load_graph_data,
        url_name='load_graph_data',
        kwargs=dict(graph_data_type='withSpam', path='/some.1/path.2')),
    ]

class UrlResolutionTest(unittest.TestCase):
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