#!/usr/bin/python
# coding=utf-8
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
################################################################################

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import create_post
from ..views import load_microblogging
import node_storage as backend

class DummyRequest():
    pass

class SimpleTest(TestCase):
    def test_post_creation(self):
        max = User()
        max.username = "max"
        max.save()

        root = backend.get_root_node()
        slot1 = backend.models.Node()
        slot1.node_type = 'slot'
        slot1.title = "Bla"
        slot1.save()
        root.append_child(slot1)

        text_node1 = backend.models.Node()
        text_node1.node_type = 'textNode'
        text_node1.title = "Whatever"
        text_node1.save()
        text1 = backend.models.Text()
        text1.node = text_node1
        text1.text = "Testtext"
        text1.author = max
        text1.save()
        slot1.append_child(text_node1)

        slot2 = backend.models.Node()
        slot2.node_type = 'slot'
        slot2.title = "Blubb"
        slot2.save()
        root.append_child(slot2)

        text_node2 = backend.models.Node()
        text_node2.node_type = 'textNode'
        text_node2.title = "Whatever"
        text_node2.save()
        text2 = backend.models.Text()
        text2.node = text_node2
        text2.text = "Testtext Nummer 2"
        text2.author = max
        text2.save()
        slot2.append_child(text_node2)

        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla gut.",max))
        posts.append(create_post("Ich finde /Blubb schlecht.", max))
        request = DummyRequest
        request.user = max
        response = load_microblogging(request,"/Bla.1",0,"older")
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
