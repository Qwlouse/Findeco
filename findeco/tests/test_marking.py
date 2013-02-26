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
from django.utils.translation import ugettext
from django.test import TestCase
from findeco.view_helpers import get_permission
from node_storage import get_root_node, Vote, SpamFlag
from node_storage.factory import create_textNode, create_slot, create_user, create_vote, create_argument, create_spam_flag

class UnFollowTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.permela = create_user("Permela", password="xxx")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(self.mid, arg_type='n')
        self.leaf1 = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf1)
        self.mid.add_derivate(self.leaf1, arg_type='n')
        self.mid2 = create_textNode("Bla derivate 2", "Blubb4", [self.hugo])
        self.slot.append_child(self.mid2)
        self.mid.add_derivate(self.mid2, arg_type='n')
        self.leaf2 = create_textNode("Bla leaf 2", "Blubb5", [self.hugo])
        self.slot.append_child(self.leaf2)
        self.mid2.add_derivate(self.leaf2, arg_type='n')
        self.follow = create_vote(self.hugo, [self.text, self.mid, self.leaf1, self.mid2, self.leaf2])

    def test_not_authenticated(self):
        response = self.client.post(reverse('unfollow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("NotAuthenticated"))

    def test_not_permitted(self):
        self.assertTrue(self.client.login(username="Permela", password="xxx"))
        response = self.client.post(reverse('unfollow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("PermissionDenied"))

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
        response = self.client.get(reverse('unfollow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),0)

    def test_unfollow_middle_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.get(reverse('unfollow_node', kwargs=dict(path="Slot.2")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),1)
        self.assertIn(self.text, self.follow.nodes.all())
        for n in [self.leaf1, self.mid, self.mid2, self.leaf2]:
            self.assertNotIn(n, self.follow.nodes.all())

class FollowTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.ulf = create_user("Ulf", password="abcde", groups=['voters'])
        self.permela = create_user("Permela", password="xxx")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(self.mid, arg_type='c', title="dagegen")
        self.leaf1 = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf1)
        self.mid.add_derivate(self.leaf1, arg_type='c', title="dagegen2")
        self.mid2 = create_textNode("Bla derivate 2", "Blubb4", [self.hugo])
        self.slot.append_child(self.mid2)
        self.mid.add_derivate(self.mid2, arg_type='c', title="dagegen")
        self.leaf2 = create_textNode("Bla leaf 2", "Blubb5", [self.hugo])
        self.slot.append_child(self.leaf2)
        self.mid2.add_derivate(self.leaf2, arg_type='c', title="dagegen")
        self.follow = create_vote(self.hugo, [self.text, self.mid, self.leaf1, self.mid2, self.leaf2])
        self.arg1 = create_argument(self.text, "con","Wrong!","Bad!",[self.hugo])

    def test_not_authenticated(self):
        response = self.client.post(reverse('follow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("NotAuthenticated"))

    def test_not_permitted(self):
        self.assertTrue(self.client.login(username="Permela", password="xxx"))
        response = self.client.post(reverse('follow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("PermissionDenied"))

    def test_follow_leaf_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Ulf", password="abcde"))
        response = self.client.get(reverse('follow_node', kwargs=dict(path="Slot.3")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),2)
        self.assertIn(self.leaf1, Vote.objects.filter(user=self.ulf).all()[0].nodes.all())
        for n in [self.text, self.mid, self.mid2, self.leaf2]:
            self.assertNotIn(n, Vote.objects.filter(user=self.ulf).all()[0].nodes.all())

    def test_follow_root_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Ulf", password="abcde"))
        response = self.client.get(reverse('follow_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),2)
        for n in [self.text, self.leaf1, self.mid, self.mid2, self.leaf2]:
            self.assertIn(n, Vote.objects.filter(user=self.ulf).all()[0].nodes.all())

    def test_follow_middle_of_derivate_tree(self):
        self.assertTrue(self.client.login(username="Ulf", password="abcde"))
        response = self.client.get(reverse('follow_node', kwargs=dict(path="Slot.2")))
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'],{})
        self.assertEqual(Vote.objects.count(),2)
        self.assertNotIn(self.text, Vote.objects.filter(user=self.ulf).all()[0].nodes.all())
        for n in [self.leaf1, self.mid, self.mid2, self.leaf2]:
            self.assertIn(n, Vote.objects.filter(user=self.ulf).all()[0].nodes.all())

class MarkSpamTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.permela = create_user("Permela", password="xxx")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(self.mid, arg_type='n')
        self.leaf = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf)
        self.mid.add_derivate(self.leaf, arg_type='n')

    def test_not_authenticated(self):
        response = self.client.post(reverse('flag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("NotAuthenticated"))

    def test_not_permitted(self):
        self.assertTrue(self.client.login(username="Permela", password="xxx"))
        response = self.client.post(reverse('flag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("PermissionDenied"))

    def test_mark_spam_root(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(reverse('flag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'], {})
        self.assertEqual(SpamFlag.objects.count(), 1)
        self.assertIn(SpamFlag.objects.all()[0], self.text.spam_flags.all())
        for n in [self.mid, self.leaf]:
            self.assertNotIn(SpamFlag.objects.all()[0], n.spam_flags.all())

    def test_mark_spam_leaf(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(reverse('flag_node', kwargs=dict(path="Slot.3")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'], {})
        self.assertEqual(SpamFlag.objects.count(), 1)
        self.assertIn(SpamFlag.objects.all()[0], self.leaf.spam_flags.all())
        for n in [self.mid, self.text]:
            self.assertNotIn(SpamFlag.objects.all()[0], n.spam_flags.all())

class UnMarkSpamTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234", groups=['voters'])
        self.permela = create_user("Permela", password="xxx")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Bla", "Blubb", [self.hugo])
        self.slot.append_child(self.text)
        self.mid = create_textNode("Bla derivate", "Blubb2", [self.hugo])
        self.slot.append_child(self.mid)
        self.text.add_derivate(self.mid, arg_type='n')
        self.leaf = create_textNode("Bla leaf 1", "Blubb3", [self.hugo])
        self.slot.append_child(self.leaf)
        self.mid.add_derivate(self.leaf, arg_type='n')
        self.text_mark = create_spam_flag(self.hugo,[self.text])
        self.mid_mark = create_spam_flag(self.hugo,[self.mid])
        self.leaf_mark = create_spam_flag(self.hugo,[self.leaf])

    def test_not_authenticated(self):
        response = self.client.post(reverse('unflag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("NotAuthenticated"))

    def test_not_permitted(self):
        self.assertTrue(self.client.login(username="Permela", password="xxx"))
        response = self.client.post(reverse('unflag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['errorResponse']['errorTitle'], ugettext("PermissionDenied"))

    def test_unmark_spam_root(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(reverse('unflag_node', kwargs=dict(path="Slot.1")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'], {})
        self.assertEqual(SpamFlag.objects.count(), 2)
        self.assertEqual(SpamFlag.objects.filter(node=self.text).count(), 0)
        for n in [self.mid, self.leaf]:
            self.assertEqual(SpamFlag.objects.filter(node=n).count(), 1)

    def test_unmark_spam_leaf(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(reverse('unflag_node', kwargs=dict(path="Slot.3")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['markNodeResponse'], {})
        self.assertEqual(SpamFlag.objects.count(), 2)
        self.assertEqual(SpamFlag.objects.filter(node=self.leaf).count(), 0)
        for n in [self.mid, self.text]:
            self.assertEqual(SpamFlag.objects.filter(node=n).count(), 1)