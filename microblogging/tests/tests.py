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
from node_storage.factory import create_slot, create_structureNode, create_textNode
from node_storage.factory import create_vote, create_argument, create_user
from ..models import create_post
from ..views import load_microblogging
import node_storage as backend
from ..models import Post

class DummyRequest():
    pass

class MicrobloggingTests(TestCase):
    def setUp(self):
        self.user_max = create_user("max")

        root = backend.get_root_node()
        slot1 = create_slot("Bla")
        root.append_child(slot1)

        text_node1 = create_textNode("Whatever","Testtext",[self.user_max])
        slot1.append_child(text_node1)

        slot2 = create_slot("Blubb")
        root.append_child(slot2)

        text_node2 = create_textNode("Whatever2","Testtext Nummer 2",[self.user_max])
        slot2.append_child(text_node2)

    def test_post_creation(self):
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla.1 gut.",self.user_max))
        posts.append(create_post("Ich finde /Blubb schlecht.", self.user_max))
        posts.append(create_post("Ich finde /Follopp schlecht.", self.user_max))

        all_posts = Post.objects.all()
        self.assertSequenceEqual(all_posts,posts)
        self.assertEqual(all_posts[0].text,'Ich finde <a href="/Bla.1">Bla.1</a> gut.')
        self.assertEqual(all_posts[0].author,self.user_max)
        print(all_posts[0].node_references)

    def test_load_microblogging(self):
        posts = []
        for i in range(25):
            posts.append(create_post("Ich finde /Bla gut.",self.user_max))
        posts.append(create_post("Ich finde /Blubb schlecht.", self.user_max))

        request = DummyRequest
        request.user = self.user_max

        response = load_microblogging(request,"Slot_4.1/SubSlot_1.1",0,"older")
        self.assertEqual(response.content,'{"errorResponse": {"errorTitle": "Illegal Path", "errorMessage": "Illegal Path: Slot_4.1/SubSlot_1.1"}}')

        response = load_microblogging(request,"/Bla.1",0,"older")
        self.assertEqual(response.status_code, 200)
        print(response)
