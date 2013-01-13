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
from django.test import Client
from django.core.urlresolvers import reverse
import unittest
import json
import itertools
from ..views import home
from jsonvalidator import JSONValidator

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

################# JSON Schemas #################################################
# The JSON responses are validated by example
integer = 1
string = "string"
boolean = True

graphDataNode_schema = {
    'index':integer,
    'authorGroup': ["user"],
    'follows':integer,
    'unFollows':integer,
    'newFollows':integer,
    'origin':"path?"
}
indexNode_schema = {
    'shortTitle':string,
    'fullTitle':string,
    'index':integer,
    'authorGroup': ["user"]
}
microblogNode_schema = {
    'microblogText':string,
    'authorGroup': ["user"],
    'microblogTime':integer,
    'microblogID':integer
}
textNode_schema = {
    'wikiText':string,
    'path':string,
    'isFollowing':boolean,
    'authorGroup': ["user"]
}
userData_schema={
    'displayName':string,
    'description':string,
    'followers':["user", None],
    'followees':["user", None]
}
loadGraphDataResponseValidator = JSONValidator({
    'success':boolean,
    'loadGraphDataResponse':{
        'graphDataChildren':[graphDataNode_schema],
        'graphDataRelated':[graphDataNode_schema, None]
    }
})
loadIndexResponseValidator = JSONValidator({
    'success':boolean,
    'loadIndexResponse':[indexNode_schema, None]
})
loadMicrobloggingResponseValidator = JSONValidator({
    'success':boolean,
    'loadMicrobloggingResponse':[microblogNode_schema, None]
})
loadTextResponseValidator = JSONValidator({
    'success':boolean,
    'loadTextResponse':{
        'paragraphs':[textNode_schema, None],
        'isFollowing':boolean,
    }
})
loadUserInfoResponseValidator = JSONValidator({
    'success':boolean,
    'loadUserInfoResponse':userData_schema
})
loadUserSettingsResponseValidator = JSONValidator({
    'success':boolean,
    'loadUserSettingsResponse':{
        'displayName':string,
        'description':string,
        'followees':["user", None],
        'blockedUsers':["user", None]
    }
})
loginResponseValidator = JSONValidator({
    'success':boolean,
    'loginResponse':userData_schema
})
logoutResponseValidator = JSONValidator({
    'success':boolean
})
markNodeResponseValidator = JSONValidator({
    'success':boolean
})
storeMicroblogPostResponseValidator = JSONValidator({
    'success':boolean
})
storeSettingsResponseValidator = JSONValidator({
    'success':boolean
})
storeTextResponseValidator = JSONValidator({
    'success':boolean
})
view_validators = {
    'load_graph_data':loadGraphDataResponseValidator,
    'load_index':loadIndexResponseValidator,
    'load_microblogging':loadMicrobloggingResponseValidator,
    'load_text':loadTextResponseValidator,
    'load_user_info':loadUserInfoResponseValidator,
    'load_user_settings':loadUserSettingsResponseValidator,
    'login':loginResponseValidator,
    'logout':logoutResponseValidator,
    'mark_node':markNodeResponseValidator,
    'store_microblog_post':storeMicroblogPostResponseValidator,
    'store_settings':storeSettingsResponseValidator,
    'store_text':storeTextResponseValidator
}

################# example paths ################################################
structure_node_paths = ['', 'foo.1', 'foo.1/bar.2']
slot_paths = ['foo', 'foo.1/bar']
argument_category_paths = ['foo.1.pro', 'foo.1/bar.2.con', 'foo.1/bar.2.neut']
argument_paths = ['foo.1.pro.3', 'foo.1/bar.2.con.4', 'foo.1/bar.2.neut.5']

################# Tests ########################################################
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

    def validate_response(self, response, view):
        response = json.loads(response)
        self.assertIn('success', response)
        if not response['success']:
            self.assertIn('error', response)
            return False
        validator = view_validators[view]
        validator.validate(response)
        return True

    def test_load_index_response_is_valid(self):
        for p in structure_node_paths:
            response = self.client.get(reverse('load_index', kwargs=dict(path=p)))
            self.validate_response(response.content, 'load_index')

    def test_load_graph_data_response_is_valid(self):
        paths = slot_paths + argument_category_paths
        graph_types = ['default', 'full', 'withSpam']
        for p, t in itertools.product(paths, graph_types):
            response = self.client.get(reverse('load_graph_data',
                kwargs=dict(path=p, graph_data_type=t)))
            self.validate_response(response.content, 'load_graph_data')

    def test_load_microblogging_response_is_valid(self):
        paths = structure_node_paths + argument_paths
        load_type = ['newer', 'older']
        for p, t in itertools.product(paths, load_type):
            result = self.client.get(reverse('load_microblogging',
                kwargs=dict(path=p, microblogging_load_type=t, select_id=1)))
            self.validate_response(result.content, 'load_microblogging')

    def test_load_text_response_is_valid(self):
        for p in structure_node_paths + slot_paths + argument_paths:
            response = self.client.get(reverse('load_text', kwargs=dict(path=p)))
            self.validate_response(response.content, 'load_text')

    def test_mark_node_response_is_valid(self):
        paths = structure_node_paths + argument_paths
        mark_type = ['spam', 'notspam', 'follow', 'unfollow']
        for p, t in itertools.product(paths, mark_type):
            response = self.client.get(reverse('mark_node',
                kwargs=dict(path=p, mark_type=t)))
            self.validate_response(response.content, 'mark_node')

    def test_load_user_info_response_is_valid(self):
        usernames = ['admin', 'fred']
        for u in usernames:
            response = self.client.get(reverse('load_user_info', kwargs=dict(name=u)))
            self.validate_response(response.content, 'load_user_info')

    def test_load_user_settings_response_is_valid(self):
        response = self.client.get(reverse('load_user_settings'))
        self.validate_response(response.content, 'load_user_settings')

    def test_logout_response_is_valid(self):
        response = self.client.get(reverse('logout'))
        self.validate_response(response.content, 'logout')

    # TODO login
    # TODO store_microblog_post
    # TODO store_settings
    # TODO store_text
