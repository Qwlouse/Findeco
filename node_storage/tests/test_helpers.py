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
#from ..path_helpers import get_path_parent, get_similar_path
from ..path_helpers import IllegalPath
from ..models import Node, Vote, Argument
from ..factory import create_slot, create_structureNode, create_textNode, create_vote

class HelpersTest(TestCase):
    def setUp(self):
        max = User()
        max.username = "Max"
        max.save()

        self.root = get_root_node()

        self.slot1 = create_slot("Slot_1")
        self.root.append_child(self.slot1)

        self.text1 = create_textNode("Irrelevant long title","My text.",[max])
        self.slot1.append_child(self.text1)

        self.slot2 = create_slot("Slot_2")
        self.root.append_child(self.slot2)

        self.text3 = create_textNode("Irrelevant long title 2","My other text.",[max])
        self.slot2.append_child(self.text3)

        self.text4 = create_textNode("Irrelevant long title 3","Yet another text.",[max])
        self.slot2.append_child(self.text4)

        self.slot3 = create_slot("Slot_3")
        self.root.append_child(self.slot3)

        self.text5 = create_textNode("Irrelevant long title 4","Yet another text. Different in the second part.",[max])
        self.slot3.append_child(self.text5)

        self.text6 = create_textNode("Irrelevant long title 5","Yet another text. Number 3.",[max])
        self.slot3.append_child(self.text6)

        create_vote(max, [self.text5])

        self.slot4 = create_slot("Slot_4")
        self.root.append_child(self.slot4)

        self.structure1 = create_structureNode("Structure1 Title","Introductory text",[max])
        self.slot4.append_child(self.structure1)

        self.structure2 = create_structureNode("Structure2 Title","Introductory text 2",[max])
        self.slot4.append_child(self.structure2)

        self.subslot1 = create_slot("SubSlot_1")
        self.structure1.append_child(self.subslot1)

        self.subslot2 = create_slot("SubSlot_2")
        self.structure2.append_child(self.subslot2)

        self.substructure1 = create_structureNode("SubStructure2 Title","Introductory text 3",[max])
        self.subslot1.append_child(self.substructure1)
        self.subslot2.append_child(self.substructure1)

        self.subsubslot1 = create_slot("SubSubSlot_1")
        self.substructure1.append_child(self.subsubslot1)

        self.subsubtext1 = create_textNode("SubSubText1 Title","Yet another text. Number 4.",[max])
        self.subsubslot1.append_child(self.subsubtext1)

        self.argument1 = Argument()
        self.argument1.node_type = 'argument'
        self.argument1.arg_type = 'pro'
        self.argument1.save()
        self.subsubtext1.append_argument(self.argument1)
        self.argument2 = Argument()
        self.argument2.node_type = 'argument'
        self.argument2.arg_type = 'neut'
        self.argument2.save()
        self.subsubtext1.append_argument(self.argument2)

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
        self.assertRaises(IllegalPath, get_node_for_path, ("Slot_4.1/SubSlot_1.1/BlubbBlubbSlot_1.1.pro.1"))
        self.assertRaises(IllegalPath, get_node_for_path, ("Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.77"))
        self.assertRaises(IllegalPath, get_node_for_path, ("Slot_4.1/SubSlot_1.8437256/SubSubSlot_1.1.pro.1"))

    def test_get_arguments_for(self):
        args = get_arguments_for(self.subsubtext1)
        self.assertSequenceEqual(args, [self.argument1, self.argument2])
        args = get_arguments_for(self.subsubtext1, 'pro')
        self.assertSequenceEqual(args, [self.argument1])
        args = get_arguments_for(self.subsubtext1, 'con')
        self.assertSequenceEqual(args, [])
        args = get_arguments_for(self.subsubtext1, 'all')
        self.assertSequenceEqual(args, [self.argument1, self.argument2])
        args = get_arguments_for(self.subsubtext1, 'neut')
        self.assertSequenceEqual(args, [self.argument2])

#    def test_get_path_parent(self):
#        node = get_path_parent(self.argument1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.1")
#        self.assertEqual(node, self.subsubtext1)
#        node = get_path_parent(self.argument1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.neut.2")
#        self.assertEqual(node, self.subsubtext1)
#        node = get_path_parent(self.argument1, "Slot_4.1/SubSlot_2.1/SubSubSlot_1.1.neut.2")
#        self.assertEqual(node, self.subsubtext1)
#        node = get_path_parent(self.subsubtext1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1")
#        self.assertEqual(node, self.subsubslot1)
#        node = get_path_parent(self.subsubtext1, "/Slot_4.1/SubSlot_1.1/SubSubSlot_1.1")
#        self.assertEqual(node, self.subsubslot1)
#        node = get_path_parent(self.subsubslot1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1")
#        self.assertEqual(node, self.substructure1)
#        node = get_path_parent(self.subsubslot1, "Slot_4.1/SubSlot_1.1/Blubb.1")
#        self.assertEqual(node, self.substructure1)
#        node = get_path_parent(self.subsubslot1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1")
#        self.assertEqual(node, self.substructure1)
#        node = get_path_parent(self.substructure1, "Slot_4.1/SubSlot_1.1")
#        self.assertEqual(node, self.subslot1)
#        node = get_path_parent(self.substructure1, "Slot_4.1/SubSlot_2.1")
#        self.assertEqual(node, self.subslot2)
#        node = get_path_parent(self.subslot1, "Slot_4.1/SubSlot_1")
#        self.assertEqual(node, self.structure1)
#        node = get_path_parent(self.subslot2, "Slot_4.1/SubSlot_2")
#        self.assertEqual(node, self.structure2)
#        node = get_path_parent(self.structure1, "Slot_4.1")
#        self.assertEqual(node, self.slot4)
#        node = get_path_parent(self.slot4, "Slot_4")
#        self.assertEqual(node, self.root)
#        node = get_path_parent(self.slot4, "")
#        self.assertEqual(node, self.root)
#        node = get_path_parent(self.slot4, "/")
#        self.assertEqual(node, self.root)

#    def test_get_similar_path(self):
#        path = get_similar_path(self.argument1, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.1")
#        print(path)
#        self.assertEqual(path, "Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.1")