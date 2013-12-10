#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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
#endregion #####################################################################
from __future__ import division, print_function, unicode_literals
import json

from django.test import TestCase

from django.core.urlresolvers import reverse
from microblogging.factory import create_post
from node_storage import get_root_node
from node_storage.factory import create_textNode, create_slot, create_user


class SearchTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla",
            "Dieser Text enthält verschiedene Suchbegriffe wie Giraffe, Huhn, Motorrad und Tisch.", [self.hugo])
        self.slot.append_child(self.text)
        self.post1 = create_post("Ich finde /Slot.1 Huhn.", self.hugo)
        self.post1 = create_post("Giraffe Huhn.", self.hugo)

    def test_username_found(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="user",search_string="Hugo")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['userResults']), 1)
        self.assertEqual(json.loads(response.content)['searchResponse']['userResults'][0]['title'], "Hugo")

    def test_username_notfound(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="user",search_string="Gerda")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['userResults']), 0)

    def test_single_word_content_found(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="content",search_string="Giraffe")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['contentResults']), 1)
        self.assertEqual(json.loads(response.content)['searchResponse']['contentResults'][0]['title'], "Bla")

    def test_single_word_content_notfound(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="content",search_string="Auto")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['contentResults']), 0)

    def test_single_word_content_found_title(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="content",search_string="Bla")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['contentResults']), 1)
        self.assertEqual(json.loads(response.content)['searchResponse']['contentResults'][0]['title'], "Bla")

    def test_single_word_microblogging_found(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="microblogging",search_string="Giraffe")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['microbloggingResults']), 1)
        response = self.client.post(reverse('search', kwargs=dict(search_fields="microblogging",search_string="Huhn")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['microbloggingResults']), 2)

    def test_single_word_microblogging_notfound(self):
        response = self.client.post(reverse('search', kwargs=dict(search_fields="microblogging",search_string="Auto")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['searchResponse']['microbloggingResults']), 0)