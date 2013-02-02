#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
from node_storage import get_root_node, Vote
from node_storage.factory import create_textNode, create_slot, create_user, create_vote, create_argument

class UnFollowTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(create_argument(), self.mid)
        self.leaf1 = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf1)
        self.mid.add_derivate(create_argument(), self.leaf1)
        self.mid2 = create_textNode("Bla derivate 2", "Blubb4", [self.hugo])
        self.slot.append_child(self.mid2)
        self.mid.add_derivate(create_argument(), self.mid2)
        self.leaf2 = create_textNode("Bla leaf 2", "Blubb5", [self.hugo])
        self.slot.append_child(self.leaf2)
        self.mid2.add_derivate(create_argument(), self.leaf2)
        self.follow = create_vote(self.hugo, [self.text, self.mid, self.leaf1, self.mid2, self.leaf2])

    def test_not_authenticated(self):
        response = self.client.post(reverse('store_text', kwargs=dict(path="Slot.1")),dict(wikiText="= Bla =\nBlubb."))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'],"NotAuthenticated")

    def test_unfollow_leaf_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.get(reverse('unfollow_node', kwargs=dict(path="Slot.3")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),1)
        for n in [self.text, self.mid, self.mid2, self.leaf2]:
            self.assertIn(n, self.follow.nodes.all())
        self.assertNotIn(self.leaf1, self.follow.nodes.all())

    def test_unfollow_root_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        pass

    def test_unfollow_middle_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        pass