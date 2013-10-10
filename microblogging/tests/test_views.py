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
from microblogging.factory import create_post
from node_storage.factory import create_user, create_nodes_for_path


class ViewTest(TestCase):

    ################# Load Microblogging All ###################################

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

    ################# Load Microblogging For Node ##############################

    def test_load_microblogging_for_node(self):
        hugo = create_user("hugo")
        create_nodes_for_path("foo.1")
        wrong_post = create_post("text", hugo, location='')
        posts = [create_post("is only posted there", hugo,
                             location='foo.1'),
                 create_post("references /foo.1 and is posted there", hugo,
                             location='foo.1'),
                 create_post("references /foo.1 but is not posted there", hugo,
                             location='')]
        response = self.client.get(reverse('load_microblogging_for_node',
                                           kwargs={'path': 'foo.1'}))
        res = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(res), 3)
        self.assertNotIn(wrong_post.id, [m["microblogID"] for m in res])
        for post in posts:
            self.assertIn(post.id, [m["microblogID"] for m in res])

    ################# Load Microblogging Timeline ##############################

    ################# Load Microblogging Mentions ##############################

    def test_load_microblogging_mentions(self):
        hugo = create_user("hugo")
        herbert = create_user("herbert")

        posts = [create_post("@hugo ", herbert, location=''),
                 create_post("@herbert @hugo", herbert, location='')]

        wrong_posts = [
            create_post("no mentions", hugo, location=''),
            create_post("@herbert", hugo, location=''),
        ]

        response = self.client.get(reverse('load_microblogging_mentions',
                                           kwargs={'name': 'hugo'}))
        res = json.loads(response.content)["loadMicrobloggingResponse"]
        self.assertEqual(len(res), 2)
        response_id_list = [m["microblogID"] for m in res]

        for post in posts:
            self.assertIn(post.id, response_id_list)

        for post in wrong_posts:
            self.assertNotIn(post.id, response_id_list)



    ################# Load Microblogging From User  ############################

    ################# Load Microblogging For Followed Nodes ####################

    ################# Load Microblogging For Authored Nodes ####################


