#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>,
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
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from django.test import TestCase
from node_storage.models import Node
from node_storage.path_helpers import get_root_node
from ..path_helpers import get_favorite_if_slot, get_ordered_children_for, get_node_for_path
from ..path_helpers import get_good_path_for_structure_node
from ..path_helpers import IllegalNodePath
from ..factory import create_slot, create_structureNode, create_textNode, create_vote, create_argument, create_user

class HelpersTest(TestCase):
    def setUp(self):
        max = create_user("Max")

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

        self.argument1 = create_argument(self.subsubtext1, arg_type='pro',text="It is good!",authors=[max])
        self.argument2 = create_argument(self.subsubtext1, arg_type='neut',text="Maybe consider something",authors=[max])

    def test_get_favorite_if_slot(self):
        n = get_favorite_if_slot(self.root)
        self.assertEqual(n, self.root)
        n = get_favorite_if_slot(self.slot1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.text1)
        self.assertEqual(n, self.text1)
        n = get_favorite_if_slot(self.slot2)
        self.assertEqual(n, self.text4)
        n = get_favorite_if_slot(Node.objects.get(id=self.slot3.id))
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
        self.assertRaises(IllegalNodePath, get_node_for_path, ("Slot_4.1/SubSlot_1.1/BlubbBlubbSlot_1.1.pro.1"))
        self.assertRaises(IllegalNodePath, get_node_for_path, ("Slot_4.1/SubSlot_1.1/SubSubSlot_1.1.pro.77"))
        self.assertRaises(IllegalNodePath, get_node_for_path, ("Slot_4.1/SubSlot_1.8437256/SubSubSlot_1.1.pro.1"))

    def test_get_good_path_for_structure_node(self):
        path = get_good_path_for_structure_node(self.subsubtext1)
        self.assertEqual("Slot_4.1/SubSlot_1.1/SubSubSlot_1.1", path)
        path = get_good_path_for_structure_node(self.text3)
        self.assertEqual("Slot_2.1", path)
        path = get_good_path_for_structure_node(self.substructure1)
        self.assertEqual("Slot_4.1/SubSlot_1.1", path)
        path = get_good_path_for_structure_node(self.substructure1, slot_path="Slot_4.2/SubSlot_2")
        self.assertEqual("Slot_4.2/SubSlot_2.1", path)
        path = get_good_path_for_structure_node(self.substructure1, slot=self.subslot2)
        self.assertEqual("Slot_4.2/SubSlot_2.1", path)
        path = get_good_path_for_structure_node(self.substructure1, slot_path="Slot_4.1/SubSlot_1")
        self.assertEqual("Slot_4.1/SubSlot_1.1", path)
        path = get_good_path_for_structure_node(self.substructure1, slot=self.subslot1)
        self.assertEqual("Slot_4.1/SubSlot_1.1", path)
