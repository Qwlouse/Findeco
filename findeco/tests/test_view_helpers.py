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

from node_storage import get_root_node
from node_storage.factory import create_user, create_slot, create_textNode, create_vote, create_structureNode, create_argument
from ..api_validation import userInfoValidator, indexNodeValidator, userSettingsValidator
from ..view_helpers import create_index_node_for_slot, create_index_node_for_argument
from ..view_helpers import create_user_info, create_user_settings, create_graph_data_node_for_structure_node

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
        self.assertIn({'displayName':'hugo'}, followers)
        self.assertIn({'displayName':'hein'}, followers)

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
        self.assertIn({'displayName':'hans'}, followees)

        user_info = create_user_info(self.hein)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 1)
        self.assertIn({'displayName':'hans'}, followees)

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
        self.assertIn({'displayName':'herbert'}, blocked)

        user_settings = create_user_settings(self.herbert)
        self.assertIn('blockedUsers', user_settings)
        blocked = user_settings['blockedUsers']
        self.assertEqual(len(blocked), 0)

        user_settings = create_user_settings(self.hein)
        self.assertIn('blockedUsers', user_settings)
        blocked = user_settings['blockedUsers']
        self.assertEqual(len(blocked), 1)
        self.assertIn({'displayName':'herbert'}, blocked)




class CreateIndexNodeForSlotTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.textnode1 = create_textNode('LangerWahlprogrammTitel', authors=[self.hans])
        self.slot1.append_child(self.textnode1)
        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode('LangerGrundsatzTitel', authors=[self.hugo])
        self.slot2.append_child(self.textnode2)
        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode('Langweilig3', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.slot3.append_child(self.textnode33)
        create_vote(self.hans, [self.textnode33])
        self.top_slots = [self.slot1, self.slot2, self.slot3]
        self.short_titles = ['Wahlprogramm', 'Grundsatzprogramm', 'Organisatorisches']
        self.full_titles = ['LangerWahlprogrammTitel', 'LangerGrundsatzTitel','Langweilig3']
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
        self.foo_pro = create_argument(type='pro', title="geil", authors=[self.hugo])
        self.foo1.append_argument(self.foo_pro)
        self.foo_neut = create_argument(type='neut', title="ist", authors=[self.hans])
        self.foo1.append_argument(self.foo_neut)
        self.foo_con = create_argument(type='con', title="geiz", authors=[self.hugo, self.hans])
        self.foo1.append_argument(self.foo_con)
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
        self.textnode1 = create_textNode('LangerWahlprogrammTitel', authors=[self.hans])
        self.slot1.append_child(self.textnode1)
        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode('LangerGrundsatzTitel', authors=[self.hugo])
        self.slot2.append_child(self.textnode2)
        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode('Langweilig3', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.textnode32d = create_textNode('Langweilig2 anders', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode32d)
        self.textnode32.add_derivate(create_argument(),self.textnode32d)
        create_vote(self.hans, [self.textnode32, self.textnode32d])
        self.slot3.append_child(self.textnode33)
        create_vote(self.hans, [self.textnode33])
        self.textnode33d = create_textNode('Langweilig3 anders', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode33d)
        self.textnode33.add_derivate(create_argument(),self.textnode33d)
        self.top_slots = [self.slot1, self.slot2, self.slot3]
        self.short_titles = ['Wahlprogramm', 'Grundsatzprogramm', 'Organisatorisches']
        self.full_titles = ['LangerWahlprogrammTitel', 'LangerGrundsatzTitel','Langweilig3']
        self.authors = [[self.hans], [self.hugo], [self.hans, self.hugo]]

    def test_text_nodes_no_path(self):
        data = create_graph_data_node_for_structure_node(self.textnode31)
        self.assertEqual(data['path'],'Organisatorisches.1')
        self.assertSequenceEqual(data['authorGroup'],[create_user_info(self.hans)])
        self.assertEqual(data['follows'],0)
        self.assertEqual(data['unFollows'],0)
        self.assertEqual(data['newFollows'],0)
        self.assertEqual(data['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32)
        self.assertEqual(data2['path'],'Organisatorisches.2')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],1)
        self.assertEqual(data2['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32d)
        self.assertEqual(data2['path'],'Organisatorisches.3')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],0)
        self.assertEqual(data2['originGroup'],['Organisatorisches.2'])
        data3 = create_graph_data_node_for_structure_node(self.textnode33)
        self.assertEqual(data3['path'],'Organisatorisches.4')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],1)
        self.assertEqual(data3['unFollows'],0)
        self.assertEqual(data3['newFollows'],1)
        self.assertEqual(data3['originGroup'],[])
        data3 = create_graph_data_node_for_structure_node(self.textnode33d)
        self.assertEqual(data3['path'],'Organisatorisches.5')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],0)
        self.assertEqual(data3['unFollows'],1)
        self.assertEqual(data3['newFollows'],0)
        self.assertEqual(data3['originGroup'],['Organisatorisches.4'])

    def test_text_nodes_slot_node(self):
        data = create_graph_data_node_for_structure_node(self.textnode31, slot=self.slot3)
        self.assertEqual(data['path'],'Organisatorisches.1')
        self.assertSequenceEqual(data['authorGroup'],[create_user_info(self.hans)])
        self.assertEqual(data['follows'],0)
        self.assertEqual(data['unFollows'],0)
        self.assertEqual(data['newFollows'],0)
        self.assertEqual(data['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32, slot=self.slot3)
        self.assertEqual(data2['path'],'Organisatorisches.2')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],1)
        self.assertEqual(data2['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32d, slot=self.slot3)
        self.assertEqual(data2['path'],'Organisatorisches.3')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],0)
        self.assertEqual(data2['originGroup'],['Organisatorisches.2'])
        data3 = create_graph_data_node_for_structure_node(self.textnode33, slot=self.slot3)
        self.assertEqual(data3['path'],'Organisatorisches.4')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],1)
        self.assertEqual(data3['unFollows'],0)
        self.assertEqual(data3['newFollows'],1)
        self.assertEqual(data3['originGroup'],[])
        data3 = create_graph_data_node_for_structure_node(self.textnode33d, slot=self.slot3)
        self.assertEqual(data3['path'],'Organisatorisches.5')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],0)
        self.assertEqual(data3['unFollows'],1)
        self.assertEqual(data3['newFollows'],0)
        self.assertEqual(data3['originGroup'],['Organisatorisches.4'])

    def test_text_nodes_path_given(self):
        data = create_graph_data_node_for_structure_node(self.textnode31, path='Organisatorisches.1')
        self.assertEqual(data['path'],'Organisatorisches.1')
        self.assertSequenceEqual(data['authorGroup'],[create_user_info(self.hans)])
        self.assertEqual(data['follows'],0)
        self.assertEqual(data['unFollows'],0)
        self.assertEqual(data['newFollows'],0)
        self.assertEqual(data['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32, path='Organisatorisches.2')
        self.assertEqual(data2['path'],'Organisatorisches.2')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],1)
        self.assertEqual(data2['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32d, path='Organisatorisches.3')
        self.assertEqual(data2['path'],'Organisatorisches.3')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],0)
        self.assertEqual(data2['originGroup'],['Organisatorisches.2'])
        data3 = create_graph_data_node_for_structure_node(self.textnode33, path='Organisatorisches.4')
        self.assertEqual(data3['path'],'Organisatorisches.4')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],1)
        self.assertEqual(data3['unFollows'],0)
        self.assertEqual(data3['newFollows'],1)
        self.assertEqual(data3['originGroup'],[])
        data3 = create_graph_data_node_for_structure_node(self.textnode33d, path='Organisatorisches.5')
        self.assertEqual(data3['path'],'Organisatorisches.5')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],0)
        self.assertEqual(data3['unFollows'],1)
        self.assertEqual(data3['newFollows'],0)
        self.assertEqual(data3['originGroup'],['Organisatorisches.4'])

    def test_text_nodes_slot_path_given(self):
        data = create_graph_data_node_for_structure_node(self.textnode31, slot_path='Organisatorisches')
        self.assertEqual(data['path'],'Organisatorisches.1')
        self.assertSequenceEqual(data['authorGroup'],[create_user_info(self.hans)])
        self.assertEqual(data['follows'],0)
        self.assertEqual(data['unFollows'],0)
        self.assertEqual(data['newFollows'],0)
        self.assertEqual(data['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32, slot_path='Organisatorisches')
        self.assertEqual(data2['path'],'Organisatorisches.2')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],1)
        self.assertEqual(data2['originGroup'],[])
        data2 = create_graph_data_node_for_structure_node(self.textnode32d, slot_path='Organisatorisches')
        self.assertEqual(data2['path'],'Organisatorisches.3')
        self.assertSequenceEqual(data2['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data2['follows'],1)
        self.assertEqual(data2['unFollows'],0)
        self.assertEqual(data2['newFollows'],0)
        self.assertEqual(data2['originGroup'],['Organisatorisches.2'])
        data3 = create_graph_data_node_for_structure_node(self.textnode33, slot_path='Organisatorisches')
        self.assertEqual(data3['path'],'Organisatorisches.4')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],1)
        self.assertEqual(data3['unFollows'],0)
        self.assertEqual(data3['newFollows'],1)
        self.assertEqual(data3['originGroup'],[])
        data3 = create_graph_data_node_for_structure_node(self.textnode33d, slot_path='Organisatorisches')
        self.assertEqual(data3['path'],'Organisatorisches.5')
        self.assertSequenceEqual(data3['authorGroup'],[create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'],0)
        self.assertEqual(data3['unFollows'],1)
        self.assertEqual(data3['newFollows'],0)
        self.assertEqual(data3['originGroup'],['Organisatorisches.4'])

    def test_text_nodes_path_and_slot_path_given(self):
        data = create_graph_data_node_for_structure_node(self.textnode31, path='Organisatorisches.1',
            slot_path='Organisatorisches')
        self.assertEqual(data['path'], 'Organisatorisches.1')
        self.assertSequenceEqual(data['authorGroup'], [create_user_info(self.hans)])
        self.assertEqual(data['follows'], 0)
        self.assertEqual(data['unFollows'], 0)
        self.assertEqual(data['newFollows'], 0)
        self.assertEqual(data['originGroup'], [])
        data2 = create_graph_data_node_for_structure_node(self.textnode32, path='Organisatorisches.2',
            slot_path='Organisatorisches')
        self.assertEqual(data2['path'], 'Organisatorisches.2')
        self.assertSequenceEqual(data2['authorGroup'], [create_user_info(self.hugo)])
        self.assertEqual(data2['follows'], 1)
        self.assertEqual(data2['unFollows'], 0)
        self.assertEqual(data2['newFollows'], 1)
        self.assertEqual(data2['originGroup'], [])
        data2 = create_graph_data_node_for_structure_node(self.textnode32d, path='Organisatorisches.3',
            slot_path='Organisatorisches')
        self.assertEqual(data2['path'], 'Organisatorisches.3')
        self.assertSequenceEqual(data2['authorGroup'], [create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data2['follows'], 1)
        self.assertEqual(data2['unFollows'], 0)
        self.assertEqual(data2['newFollows'], 0)
        self.assertEqual(data2['originGroup'], ['Organisatorisches.2'])
        data3 = create_graph_data_node_for_structure_node(self.textnode33, path='Organisatorisches.4',
            slot_path='Organisatorisches')
        self.assertEqual(data3['path'], 'Organisatorisches.4')
        self.assertSequenceEqual(data3['authorGroup'], [create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'], 1)
        self.assertEqual(data3['unFollows'], 0)
        self.assertEqual(data3['newFollows'], 1)
        self.assertEqual(data3['originGroup'], [])
        data3 = create_graph_data_node_for_structure_node(self.textnode33d, path='Organisatorisches.5',
            slot_path='Organisatorisches')
        self.assertEqual(data3['path'], 'Organisatorisches.5')
        self.assertSequenceEqual(data3['authorGroup'], [create_user_info(self.hans), create_user_info(self.hugo)])
        self.assertEqual(data3['follows'], 0)
        self.assertEqual(data3['unFollows'], 1)
        self.assertEqual(data3['newFollows'], 0)
        self.assertEqual(data3['originGroup'], ['Organisatorisches.4'])