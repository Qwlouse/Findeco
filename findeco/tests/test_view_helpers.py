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
from django.test import TestCase
from findeco.view_helpers import get_is_following

from node_storage import get_root_node, Node
from node_storage.factory import create_user, create_slot, create_textNode
from node_storage.factory import create_vote, create_structureNode
from node_storage.factory import create_argument
from ..api_validation import userInfoValidator, indexNodeValidator
from ..api_validation import userSettingsValidator
from ..view_helpers import create_index_node_for_slot, create_user_settings
from ..view_helpers import create_index_node_for_argument, create_user_info
from ..view_helpers import create_graph_data_node_for_structure_node
from ..view_helpers import store_structure_node, store_argument, store_derivate


class CreateUsersInfoTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', "he's a jolly good fellow")
        self.hugo = create_user('hugo', "nodescription")
        self.hein = create_user('hein', "password1")
        self.users = [self.hans, self.hugo, self.hein]

        self.hugo.profile.followees.add(self.hans.profile)
        self.hein.profile.followees.add(self.hans.profile)

    def test_create_user_info_validates(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertTrue(userInfoValidator.validate(user_info))

    def test_create_user_info_contains_correct_username(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertEqual(user_info['displayName'], user.username)

    def test_create_user_info_contains_correct_description(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertEqual(user_info['description'], user.profile.description)

    def test_create_user_info_contains_correct_followers(self):
        user_info = create_user_info(self.hans)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 2)
        self.assertIn({'displayName': 'hugo'}, followers)
        self.assertIn({'displayName': 'hein'}, followers)

        user_info = create_user_info(self.hugo)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 0)

        user_info = create_user_info(self.hein)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 0)

    def test_create_user_info_contains_correct_followees(self):
        user_info = create_user_info(self.hans)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 0)

        user_info = create_user_info(self.hugo)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 1)
        self.assertIn({'displayName': 'hans'}, followees)

        user_info = create_user_info(self.hein)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 1)
        self.assertIn({'displayName': 'hans'}, followees)


class CreateUserSettingsTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.herbert = create_user('herbert')
        self.hein = create_user('hein')
        self.hans.profile.blocked.add(self.herbert.profile)
        self.hein.profile.blocked.add(self.herbert.profile)
        self.users = [self.hans, self.herbert, self.hein]

    def test_return_value_validates(self):
        for user in self.users:
            user_settings = create_user_settings(user)
            self.assertTrue(userSettingsValidator.validate(user_settings))

    def test_contains_correct_blocked_users(self):
        user_settings = create_user_settings(self.hans)
        self.assertIn('blockedUsers', user_settings)
        blocked = user_settings['blockedUsers']
        self.assertEqual(len(blocked), 1)
        self.assertIn({'displayName': 'herbert'}, blocked)

        user_settings = create_user_settings(self.herbert)
        self.assertIn('blockedUsers', user_settings)
        blocked = user_settings['blockedUsers']
        self.assertEqual(len(blocked), 0)

        user_settings = create_user_settings(self.hein)
        self.assertIn('blockedUsers', user_settings)
        blocked = user_settings['blockedUsers']
        self.assertEqual(len(blocked), 1)
        self.assertIn({'displayName': 'herbert'}, blocked)


class CreateIndexNodeForSlotTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.textnode1 = create_textNode('LangerWahlprogrammTitel',
                                         authors=[self.hans])
        self.slot1.append_child(self.textnode1)
        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode('LangerGrundsatzTitel',
                                         authors=[self.hugo])
        self.slot2.append_child(self.textnode2)
        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode('Langweilig3',
                                          authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.slot3.append_child(self.textnode33)
        create_vote(self.hans, [self.textnode33])
        self.top_slots = [self.slot1, self.slot2, self.slot3]
        self.short_titles = ['Wahlprogramm', 'Grundsatzprogramm',
                             'Organisatorisches']
        self.full_titles = ['LangerWahlprogrammTitel', 'LangerGrundsatzTitel',
                            'Langweilig3']
        self.authors = [[self.hans], [self.hugo], [self.hans, self.hugo]]

    def test_index_node_validates(self):
        for slot in self.top_slots:
            index_node = create_index_node_for_slot(slot)
            self.assertTrue(indexNodeValidator.validate(index_node))

    def test_index_node_contains_correct_short_title(self):
        for slot, short_title in zip(self.top_slots, self.short_titles):
            index_node = create_index_node_for_slot(slot)
            self.assertIn('shortTitle', index_node)
            self.assertEqual(index_node['shortTitle'], short_title)

    def test_index_node_contains_correct_full_title(self):
        for slot, full_title in zip(self.top_slots, self.full_titles):
            index_node = create_index_node_for_slot(slot)
            self.assertIn('fullTitle', index_node)
            self.assertEqual(index_node['fullTitle'], full_title)

    def test_index_node_contains_correct_index(self):
        for slot, index in zip(self.top_slots, [1, 1, 3]):
            index_node = create_index_node_for_slot(slot)
            self.assertIn('index', index_node)
            self.assertEqual(index_node['index'], index)

    def test_index_node_contains_correct_author_group(self):
        for slot, authors in zip(self.top_slots, self.authors):
            index_node = create_index_node_for_slot(slot)
            self.assertIn('authorGroup', index_node)
            author_group = index_node['authorGroup']
            for user in authors:
                self.assertIn(create_user_info(user), author_group)


class CreateIndexNodeForArgumentTest(TestCase):
    def setUp(self):
        self.hugo = create_user('hugo')
        self.hans = create_user('hans')
        # create nodes
        self.root = get_root_node()
        self.foo = create_slot('foo')
        self.foo1 = create_structureNode('FooooBar')
        # add arguments
        self.foo_pro = create_argument(self.foo1, arg_type='pro', title="geil",
                                       authors=[self.hugo])
        self.foo_neut = create_argument(self.foo1, arg_type='neut', title="ist",
                                        authors=[self.hans])
        self.foo_con = create_argument(self.foo1, arg_type='con', title="geiz",
                                       authors=[self.hugo, self.hans])
        # summary variables
        self.foo_arguments = [self.foo_pro, self.foo_neut, self.foo_con]
        self.arg_titles = ['geil', 'ist', 'geiz']
        self.arg_authors = [[self.hugo], [self.hans], [self.hugo, self.hans]]

    def test_index_node_validates(self):
        for arg in self.foo_arguments:
            index_node = create_index_node_for_argument(arg, self.foo1)
            self.assertTrue(indexNodeValidator.validate(index_node))

    def test_index_node_contains_arg_type_as_short_title(self):
        for arg, arg_type in zip(self.foo_arguments, ['pro', 'neut', 'con']):
            index_node = create_index_node_for_argument(arg, self.foo1)
            self.assertIn('shortTitle', index_node)
            self.assertEqual(index_node['shortTitle'], arg_type)

    def test_index_node_contains_correct_full_title(self):
        for arg, full_title in zip(self.foo_arguments, self.arg_titles):
            index_node = create_index_node_for_argument(arg, self.foo1)
            self.assertIn('fullTitle', index_node)
            self.assertEqual(index_node['fullTitle'], full_title)

    def test_index_node_contains_correct_index(self):
        for arg, index in zip(self.foo_arguments, [1, 2, 3]):
            index_node = create_index_node_for_argument(arg, self.foo1)
            self.assertIn('index', index_node)
            self.assertEqual(index_node['index'], index)

    def test_index_node_contains_correct_author_group(self):
        for arg, authors in zip(self.foo_arguments, self.arg_authors):
            index_node = create_index_node_for_argument(arg, self.foo1)
            self.assertIn('authorGroup', index_node)
            author_group = index_node['authorGroup']
            for user in authors:
                self.assertIn(create_user_info(user), author_group)


class CreateGraphDataNodeForStructureNodeTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.textnode1 = create_textNode('LangerWahlprogrammTitel',
                                         authors=[self.hans])
        self.slot1.append_child(self.textnode1)
        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode('LangerGrundsatzTitel',
                                         authors=[self.hugo])
        self.slot2.append_child(self.textnode2)
        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode('Langweilig3',
                                          authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.textnode32d = create_textNode('Langweilig2 anders',
                                           authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode32d)
        self.textnode32.add_derivate(self.textnode32d)
        create_vote(self.hans, [self.textnode32, self.textnode32d])
        self.slot3.append_child(self.textnode33)
        self.textnode33d = create_textNode('Langweilig3 anders',
                                           authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode33d)
        self.textnode33.add_derivate(self.textnode33d)
        create_vote(self.hans, [self.textnode33])
        self.nodes = [self.textnode31, self.textnode32, self.textnode32d,
                      self.textnode33, self.textnode33d]
        self.authorGroups = [[create_user_info(self.hans)],
                             [create_user_info(self.hugo)],
                             [create_user_info(self.hans),
                              create_user_info(self.hugo)],
                             [create_user_info(self.hans),
                              create_user_info(self.hugo)],
                             [create_user_info(self.hans),
                              create_user_info(self.hugo)]]
        self.follows = [0, 1, 1, 1, 0]
        self.unFollows = [0, 0, 0, 0, 1]
        self.newFollows = [0, 1, 0, 1, 0]
        self.originGroups = [[], [], ['Organisatorisches.2'], [],
                                     ['Organisatorisches.4']]

    def test_text_nodes_no_path(self):
        for i in range(5):
            data = create_graph_data_node_for_structure_node(self.nodes[i])
            self.assertEqual(data['path'], 'Organisatorisches.' + str(i + 1))
            self.assertSequenceEqual(data['authorGroup'], self.authorGroups[i])
            self.assertEqual(data['follows'], self.follows[i])
            self.assertEqual(data['unFollows'], self.unFollows[i])
            self.assertEqual(data['newFollows'], self.newFollows[i])
            self.assertEqual(data['originGroup'], self.originGroups[i])

    def test_text_nodes_slot_node(self):
        for i in range(5):
            data = create_graph_data_node_for_structure_node(self.nodes[i],
                                                             slot=self.slot3)
            self.assertEqual(data['path'], 'Organisatorisches.' + str(i + 1))
            self.assertSequenceEqual(data['authorGroup'], self.authorGroups[i])
            self.assertEqual(data['follows'], self.follows[i])
            self.assertEqual(data['unFollows'], self.unFollows[i])
            self.assertEqual(data['newFollows'], self.newFollows[i])
            self.assertEqual(data['originGroup'], self.originGroups[i])

    def test_text_nodes_path_given(self):
        for i in range(5):
            data = create_graph_data_node_for_structure_node(
                self.nodes[i],
                path='Organisatorisches.' + str(i + 1))
            self.assertEqual(data['path'], 'Organisatorisches.' + str(i + 1))
            self.assertSequenceEqual(data['authorGroup'], self.authorGroups[i])
            self.assertEqual(data['follows'], self.follows[i])
            self.assertEqual(data['unFollows'], self.unFollows[i])
            self.assertEqual(data['newFollows'], self.newFollows[i])
            self.assertEqual(data['originGroup'], self.originGroups[i])

    def test_text_nodes_slot_path_given(self):
        for i in range(5):
            data = create_graph_data_node_for_structure_node(
                self.nodes[i],
                slot_path='Organisatorisches')
            self.assertEqual(data['path'], 'Organisatorisches.' + str(i + 1))
            self.assertSequenceEqual(data['authorGroup'], self.authorGroups[i])
            self.assertEqual(data['follows'], self.follows[i])
            self.assertEqual(data['unFollows'], self.unFollows[i])
            self.assertEqual(data['newFollows'], self.newFollows[i])
            self.assertEqual(data['originGroup'], self.originGroups[i])

    def test_text_nodes_path_and_slot_path_given(self):
        for i in range(5):
            data = create_graph_data_node_for_structure_node(
                self.nodes[i],
                path='Organisatorisches.' + str(i + 1),
                slot_path='Organisatorisches')
            self.assertEqual(data['path'], 'Organisatorisches.' + str(i + 1))
            self.assertSequenceEqual(data['authorGroup'], self.authorGroups[i])
            self.assertEqual(data['follows'], self.follows[i])
            self.assertEqual(data['unFollows'], self.unFollows[i])
            self.assertEqual(data['newFollows'], self.newFollows[i])
            self.assertEqual(data['originGroup'], self.originGroups[i])


class StoreStructureNodeTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.mustermann = create_user("Mustermann")
        self.slot = create_slot("Flopp")
        self.root.append_child(self.slot)
        self.text1 = create_textNode("Initial Text", "Dumdidum",
                                     [self.mustermann])
        self.slot.append_child(self.text1)

    def test_store_valid_path(self):
        node, path = store_structure_node("Flopp.1",
                                          "= Bla =\nText\n== Blubb ==\nText 2",
                                          self.mustermann)
        self.assertEqual(node.title, "Bla")
        self.assertEqual(path, "Flopp.2")
        self.assertEqual(len(self.slot.children.all()), 2)
        self.assertEqual(self.slot.children.all()[1].title, "Bla")
        self.assertEqual(self.slot.children.all()[1].text.text, "Text")
        self.assertEqual(self.slot.children.all()[1].children.all()[0].title,
                         "Blubb")
        self.assertEqual(
            self.slot.children.all()[1].children.all()[0].children.all()[
                0].title, "Blubb")
        self.assertEqual(
            self.slot.children.all()[1].children.all()[0].children.all()[
                0].text.text, "Text 2")
        self.assertIn(self.mustermann,
                      self.slot.children.all()[1].text.authors.all())

    def test_store_non_existent_path(self):
        node, path = store_structure_node("Flopp.4576",
                                          "= Bla =\nText\n== Blubb ==\nText 2",
                                          self.mustermann)
        self.assertEqual(node.title, "Bla")
        self.assertEqual(path, "Flopp.2")
        self.assertEqual(len(self.slot.children.all()), 2)
        self.assertEqual(self.slot.children.all()[1].title, "Bla")
        self.assertEqual(self.slot.children.all()[1].text.text, "Text")
        self.assertEqual(self.slot.children.all()[1].children.all()[0].title,
                         "Blubb")
        self.assertEqual(
            self.slot.children.all()[1].children.all()[0].children.all()[
                0].title, "Blubb")
        self.assertEqual(
            self.slot.children.all()[1].children.all()[0].children.all()[
                0].text.text, "Text 2")
        self.assertIn(self.mustermann,
                      self.slot.children.all()[1].text.authors.all())


class StoreArgumentTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.mustermann = create_user("Mustermann")
        self.slot = create_slot("Flopp")
        self.root.append_child(self.slot)
        self.text1 = create_textNode("Initial Text", "Dumdidum",
                                     [self.mustermann])
        self.slot.append_child(self.text1)
        self.text2 = create_textNode("Secondary Text", "Dudelda",
                                     [self.mustermann])
        self.text1.add_derivate(self.text2)

    def test_store_con(self):
        self.assertEqual(
            store_argument("Flopp.1", "= Avast =\nAgainst it!", "con",
                           self.mustermann), "Flopp.1.con.1")
        self.assertEqual(self.text1.arguments.count(), 1)
        self.assertEqual(self.text1.arguments.all()[0].title, "Avast")
        self.assertEqual(self.text1.arguments.all()[0].text.text,
                         "= Avast =\nAgainst it!")
        self.assertEqual(self.text1.arguments.all()[0].arg_type, "c")
        self.assertIn(self.mustermann,
                      self.text1.arguments.all()[0].text.authors.all())

    def test_derivation(self):
        self.assertEqual(
            store_argument("Flopp.1", "= Avast =\nAgainst it!", "con",
                           self.mustermann), "Flopp.1.con.1")
        self.assertEqual(self.text1.arguments.count(), 1)
        self.assertEqual(self.text2.arguments.count(), 1)
        self.assertEqual(self.text2.arguments.all()[0].title, "Avast")
        self.assertEqual(self.text2.arguments.all()[0].sources.count(), 1)
        self.assertEqual(self.text2.arguments.all()[0].sources.all()[0].pk,
                         self.text1.arguments.all()[0].pk)

    def test_auto_follow(self):
        self.assertEqual(
            store_argument("Flopp.1", "= Avast =\nAgainst it!", "con",
                           self.mustermann), "Flopp.1.con.1")
        self.assertEqual(self.text1.arguments.count(), 1)
        self.assertEqual(self.text1.arguments.all()[0].votes.count(), 1)
        self.assertEqual(self.text2.arguments.count(), 1)
        self.assertEqual(self.text2.arguments.all()[0].votes.count(), 1)
        self.assertEqual(self.text1.arguments.all()[0].votes.all()[0].pk,
                         self.text2.arguments.all()[0].votes.all()[0].pk)


class StoreDerivateTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.mustermann = create_user("Mustermann")
        self.slot = create_slot("Flopp")
        self.root.append_child(self.slot)
        self.text1 = create_textNode("Initial Text", "Dumdidum",
                                     [self.mustermann])
        self.slot.append_child(self.text1)
        create_vote(self.mustermann, [self.text1])

    def test_store_derivate(self):
        self.assertEqual(
            store_derivate("Flopp.1", "= Avast =\nAgainst it!", "con",
                           "= Bla =\nText\n== Blubb ==\nText 2",
                           self.mustermann), "Flopp.2")
        self.assertEqual(self.text1.derivates.count(), 1)
        self.assertEqual(self.text1.derivates.all()[0].title, "Bla")
        self.assertEqual(self.text1.arguments.all()[0].title, "Avast")
        self.assertEqual(self.text1.derivates.all()[0].votes.count(), 1)

    def test_auto_follows(self):
        self.assertEqual(
            store_derivate("Flopp.1", "= Avast =\nAgainst it!", "con",
                           "= Bla =\nText\n== Blubb ==\nText 2",
                           self.mustermann), "Flopp.2")
        self.assertEqual(Node.objects.filter(title="Bla").count(), 1)
        self.assertEqual(
            Node.objects.filter(title="Bla").all()[0].votes.count(), 1)
        self.assertEqual(self.text1.arguments.count(), 1)
        self.assertEqual(self.text1.arguments.all()[0].votes.count(), 1)
        self.assertEqual(
            Node.objects.filter(title="Bla").all()[0].arguments.count(), 1)
        self.assertEqual(
            Node.objects.filter(title="Bla").all()[0].arguments.all()[
                0].votes.count(), 0)


class GetIsFollowingTest(TestCase):
    def setUp(self):
        self.n = create_structureNode("woot")
        self.n1 = create_structureNode("foo1")
        self.n2 = create_structureNode("foo2")
        self.n1.add_derivate(self.n2)
        self.hugo = create_user("hugo")
        self.v = create_vote(self.hugo, [self.n1, self.n2])

    def test_on_node_without_follow_is_0(self):
        self.assertEqual(get_is_following(self.hugo.id, self.n), 0)

    def test_on_node_with_transitive_follow_is_1(self):
        self.assertEqual(get_is_following(self.hugo.id, self.n2), 1)

    def test_on_node_with_explicit_follow_is_2(self):
        self.assertEqual(get_is_following(self.hugo.id, self.n1), 2)