#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
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
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, print_function, unicode_literals
import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from findeco.api_validation import validate_response
from microblogging.factory import create_post
from node_storage.factory import create_user, create_nodes_for_path


class ViewTest(TestCase):
    def test_load_microblogging_all_status_ok(self):
        response = self.client.get(reverse('load_microblogging_all'))
        self.assertEqual(response.status_code, 200)

    def test_load_microblogging_all_returns_valid_json_response(self):
        hugo = create_user("hugo")
        create_post("text", hugo, location='')
        response = self.client.get(reverse('load_microblogging_all'))
        validate_response(response.content, 'load_microblogging')

    def test_load_microblogging_all_loads_all_microblogging(self):
        hugo = create_user("hugo")
        herbert = create_user("herbert")
        create_nodes_for_path("foo.1")
        posts = [create_post("text", hugo, location=''),
                 create_post("text3", hugo, location='foo.1'),
                 create_post("text2", herbert, location='foo.1')]
        response = self.client.get(reverse('load_microblogging_all'))
        res = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(res), 3)
        ids = [m["microblogID"] for m in res]
        for p in posts:
            self.assertIn(p.id, ids)




