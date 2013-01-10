#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
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
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User
from node_storage.path_helpers import get_root_node
from ..path_helpers import get_favorite_if_slot, get_ordered_children_for, get_node_for_path, get_arguments_for
from ..models import Node, Vote, Text, Argument

class HelpersTest(TestCase):
    def setUp(self):
        max = User()
        max.username = "Max"
        max.save()

        self.root = get_root_node()

        self.slot1 = Node()
        self.slot1.node_type = 'slot'
        self.slot1.save()
        slot1_title = Text()
        slot1_title.text = "Slot_1"
        slot1_title.node = self.slot1
        slot1_title.save()
        slot1_title.authors.add(max)
        slot1_title.save()
        self.root.append_child(self.slot1)

        self.text1 = Node()
        self.text1.node_type = 'textNode'
        self.text1.save()
        self.slot1.append_child(self.text1)

        self.slot2 = Node()
        self.slot2.node_type = 'slot'
        self.slot2.save()
        slot2_title = Text()
        slot2_title.text = "Slot_2"
        slot2_title.node = self.slot2
        slot2_title.save()
        slot2_title.authors.add(max)
        slot2_title.save()
        self.root.append_child(self.slot2)

        self.text3 = Node()
        self.text3.node_type = 'textNode'
        self.text3.save()
        self.slot2.append_child(self.text3)

        self.text4 = Node()
        self.text4.node_type = 'textNode'
        self.text4.save()
        self.slot2.append_child(self.text4)

        self.slot3 = Node()
        self.slot3.node_type = 'slot'
        self.slot3.save()
        slot3_title = Text()
        slot3_title.text = "Slot_3"
        slot3_title.node = self.slot3
        slot3_title.save()
        slot3_title.authors.add(max)
        slot3_title.save()
        self.root.append_child(self.slot3)

        self.text5 = Node()
        self.text5.node_type = 'textNode'
        self.text5.save()
        self.slot3.append_child(self.text5)

        self.text6 = Node()
        self.text6.node_type = 'textNode'
        self.text6.save()
        self.slot3.append_child(self.text6)

        v1 = Vote()
        v1.user = max
        v1.save()
        v1.nodes.add(self.text5)
        v1.save()

        self.slot4 = Node()
        self.slot4.node_type = 'slot'
        self.slot4.save()
        slot4_title = Text()
        slot4_title.text = "Slot_4"
        slot4_title.node = self.slot4
        slot4_title.save()
        slot4_title.authors.add(max)
        slot4_title.save()
        self.root.append_child(self.slot4)

        self.structure1 = Node()
        self.structure1.node_type = 'structureNode'
        self.structure1.save()
        self.slot4.append_child(self.structure1)

        self.subslot1 = Node()
        self.subslot1.node_type = 'slot'
        self.subslot1.save()
        subslot1_title = Text()
        subslot1_title.text = "SubSlot_1"
        subslot1_title.node = self.subslot1
        subslot1_title.save()
        subslot1_title.authors.add(max)
        subslot1_title.save()
        self.structure1.append_child(self.subslot1)

        self.substructure1 = Node()
        self.substructure1.node_type = 'structureNode'
        self.substructure1.save()
        self.subslot1.append_child(self.substructure1)

        self.subsubslot1 = Node()
        self.subsubslot1.node_type = 'slot'
        self.subsubslot1.save()
        subsubslot1_title = Text()
        subsubslot1_title.text = "SubSubSlot_1"
        subsubslot1_title.node = self.subsubslot1
        subsubslot1_title.save()
        subsubslot1_title.authors.add(max)
        subsubslot1_title.save()
        self.substructure1.append_child(self.subsubslot1)

        self.subsubtext1 = Node()
        self.subsubtext1.node_type = 'textNode'
        self.subsubtext1.save()
        self.subsubslot1.append_child(self.subsubtext1)

        self.argument1 = Argument()
        self.argument1.node_type = 'argument'
        self.argument1.arg_type = 'pro'
        self.argument1.save()
        self.subsubtext1.append_argument(self.argument1)

    def test_get_favorite_if_slot(self):
        n = get_favorite_if_slot(self.root)
        self.assertEqual(n, self.root)
        n = get_favorite_if_slot(self.slot1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.text1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.slot2)
        self.assertEqual(n, self.text4)
        n = get_favorite_if_slot(self.slot3)
        self.assertEqual(n, self.text5)

    def test_get_ordered_children_for(self):
        list = get_ordered_children_for(self.slot3)
        self.assertSequenceEqual(list, [self.text5, self.text6])
        list = get_ordered_children_for(self.slot2)
        self.assertSequenceEqual(list, [self.text3, self.text4])
        list = get_ordered_children_for(self.root)
        self.assertSequenceEqual(list, [self.slot1, self.slot2, self.slot3, self.slot4])
        list = get_ordered_children_for(self.subsubtext1)
        self.assertSequenceEqual(list, [])

    def test_get_node_for_path(self):
        node = get_node_for_path("")
        self.assertEqual(node, self.root)
        node = get_node_for_path("Slot_1")
        self.assertEqual(node, self.slot1)
        node = get_node_for_path("Slot_1.1")
        self.assertEqual(node, self.text1)
        node = get_node_for_path("Slot_2.1")
        self.assertEqual(node, self.text3)
        node = get_node_for_path("Slot_2.2")
        self.assertEqual(node, self.text4)
        node = get_node_for_path("Slot_4.1/SubSlot_1.1/SubSubSlot_1.1")
        self.assertEqual(node, self.subsubtext1)
        node = get_node_for_path("Slot_4.1/SubSlot_1.1/SubSubSlot_1")
        self.assertEqual(node, self.subsubslot1)
        node = get_node_for_path("Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.1")
        self.assertEqual(node, self.argument1)

    def test_get_arguments_for(self):
        args = get_arguments_for(self.subsubtext1)
        self.assertSequenceEqual(args, [self.argument1])
        args = get_arguments_for(self.subsubtext1, 'pro')
        self.assertSequenceEqual(args, [self.argument1])
        args = get_arguments_for(self.subsubtext1, 'con')
        self.assertSequenceEqual(args, [])