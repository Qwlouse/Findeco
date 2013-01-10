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
    def test_home_view_status_ok(self):
        client = Client()
        response = client.get(reverse(home, kwargs=dict(path='')))
        self.assertEqual(response.status_code, 200)

    #@unittest.skip('skip for the moment')
    def test_all_api_views_return_json(self):
        User.objects.create_user('fred', 'fake@pukkared.com', 'secret')
        client = Client()
        client.login(username='fred', password='secret')
        for v, kwargs in views:
            client.get(reverse(v, kwargs=kwargs))

    def test_load_index_view(self):
        pass