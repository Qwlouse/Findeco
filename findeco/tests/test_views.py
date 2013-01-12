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
from __future__ import division, print_function, unicode_literals
from django.contrib.auth.models import User
from django.test import Client
from django.core.urlresolvers import reverse
import unittest
import json
import itertools
from ..views import home

views = [('load_index', dict(path='')),
         ('load_user_settings', dict()),
         ('load_graph_data', dict(graph_data_type='default', path='')),
         ('load_graph_data', dict(graph_data_type='full', path='')),
         ('load_graph_data', dict(graph_data_type='withSpam', path='')),
         ('load_microblogging', dict(path='', select_id=0, microblogging_load_type='newer')),
         ('load_microblogging', dict(path='', select_id=0, microblogging_load_type='older')),
         ('load_text', dict(path='')),
         ('load_user_info', dict(name='admin')),
         ('logout', dict()),
         ('mark_node', dict(path='', mark_type='spam')),
         ('mark_node', dict(path='', mark_type='notspam')),
         ('mark_node', dict(path='', mark_type='follow')),
         ('mark_node', dict(path='', mark_type='unfollow')),
         ('store_microblog_post', dict(path='')),
         ('store_settings', dict()),
         ('store_text', dict(path=''))
]


class ViewTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login()

    def test_home_view_status_ok(self):
        response = self.client.get(reverse(home, kwargs=dict(path='')))
        self.assertEqual(response.status_code, 200)

    def test_all_api_views_return_json(self):
        for v, kwargs in views:
            response = self.client.get(reverse(v, kwargs=kwargs))
            res = json.loads(response.content)
            self.assertIsNotNone(res)

    def validate_format(self, entry, format):
        for title, cls in format:
                self.assertIn(title, entry)
                self.assertIsInstance(entry[title], cls)

    def validate_load_index_response(self, response):
        self.assertIn('success', response)
        if not response['success']:
            self.assertIn('error', response)
            return False
        self.validate_format(response, [('loadIndexResponse', list)])
        entry_format = [('shortTitle', unicode),
                        ('index', int),
                        ('fullTitle', unicode),
                        ('authorGroup', list)]
        for entry in response['loadIndexResponse']:
            self.validate_format(entry, entry_format)
        return True

    def validate_graph_data_node(self, node):
        self.validate_format(node, [('index', int),
                                    ('authorGroup', list),
                                    ('follows', int),
                                    ('unFollows', int),
                                    ('newFollows', int),
                                    ('origin', unicode)])

    def validate_load_graph_data_response(self, response):
        self.assertIn('success', response)
        if not response['success']:
            self.assertIn('error', response)
            return False
        self.validate_format(response, [('loadGraphDataResponse', dict)])
        data = response['loadGraphDataResponse']
        self.validate_format(data, [('graphDataChildren', list),
                                    ('graphDataRelated', list)])
        children = data['graphDataChildren']
        related = data['graphDataRelated']
        for node in children + related:
            self.validate_graph_data_node(node)
        return True


    def test_load_index_response_is_valid(self):
        paths = ['', 'foo', 'foo.1', 'foo.1.pro', 'foo.1.pro.1', 'foo.1/bar']
        for p in paths:
            result = self.client.get(reverse('load_index', kwargs=dict(path=p)))
            response = json.loads(result.content)
            self.validate_load_index_response(response)

    def test_load_graph_data_response_is_valid(self):
        paths = ['foo', 'foo.1.pro', 'foo.1/bar']
        graph_types = ['default', 'full', 'with_spam']
        for p, t in itertools.product(paths, graph_types):
            result = self.client.get(reverse('load_graph_data',
                kwargs=dict(path=p, graph_data_type='default')))
            response = json.loads(result.content)
            self.validate_load_graph_data_response(response)
