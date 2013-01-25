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
from node_storage.structure_parser import validate_structure_schema
from ..structure_parser import strip_accents, substitute_umlauts, parse
from ..structure_parser import remove_unallowed_chars, turn_into_valid_short_title
from ..structure_parser import create_structure_from_structure_node_schema
from ..factory import create_user, create_slot
from ..path_helpers import get_root_node
from ..models import Node

class StructureParserTest(TestCase):
    def test_strip_accents(self):
        self.assertEqual(strip_accents("aäàáâeèéêiìíîoöòóôuüùúû"),
                                       "aaaaaeeeeiiiiooooouuuuu")

    def test_substitute_umlauts(self):
        self.assertEqual(substitute_umlauts("Haßloch"), "Hassloch")
        self.assertEqual(substitute_umlauts("HAẞLOCH"), "HASSLOCH")
        self.assertEqual(substitute_umlauts("Köln"), "Koeln")
        self.assertEqual(substitute_umlauts("Ülm"), "Uelm")
        self.assertEqual(substitute_umlauts("Ärger"), "Aerger")

    def test_remove_unallowed_chars(self):
        self.assertEqual(remove_unallowed_chars("abc()[]{}<>?!.,:;+^`~|$#%def"), "abcdef")

    def test_remove_unallowde_chars_keeps_allowed_chars(self):
        valid = "abcdefghijklmnopqrstuvwxyz-1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertEqual(remove_unallowed_chars(valid), valid)

    def test_turn_into_valid_short_title(self):
        titles = [
            ("schöner Titel was?", "schoener_Titel_was"),
            ("viiiiiieeeeeel zuuuuuuu laaaaaaaang", "viiiiiieeeeeel_zuuuu"),
            ("viel )()()(()()( zu {}{}{}{ lang", "viel_zu_lang"),
            ("","1"),
            ("N0body is as L€€+.a$.m3", "N0body_is_as_Lam3")
        ]
        for t, st in titles:
            self.assertEqual(turn_into_valid_short_title(t), st)

    def test_validate_structure_schema_on_simple_example(self):
        simple = dict(title="foo", short_title="foo", text="und bar und so", children=[])
        self.assertTrue(validate_structure_schema(simple))

    def test_validate_structure_schema_on_simple_example(self):
        invalid = dict(title="foo", text="und bar und so", children=[])
        self.assertRaises(AssertionError, validate_structure_schema, invalid)

    def test_structure_parser(self):
        wiki = """
        = Titel =
        einleitungstext
        == slot1 ==
        text
        == Toller Slot § slot2 ==
        mehr text
        """
        s = parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        schema = {'short_title': "foo",
                  'title': "Titel",
                  'text': "einleitungstext",
                  'children': [
                      {'short_title': "slot1",
                       'title': "slot1",
                       'text': "text",
                       'children': []},
                      {'short_title': "slot2",
                       'title': "Toller Slot",
                       'text': "mehr text",
                       'children': []},
                      ]}
        self.assertEqual(s,schema)

class CreateStructureFromStructureNodeSchemaTest(TestCase):
    def setUp(self):
        self.hugo = create_user("Hugo")
        self.root = get_root_node()
        self.slot1 = create_slot("Slot_1")
        self.root.append_child(self.slot1)

    def test_create_structure_from_structure_node_schema_without_origin_group(self):
        schema = {'short_title': "Ignored",
                  'title': "My first structure Node",
                  'text': "This is the text.",
                  'children': [
                      {'short_title': "Layer_1a",
                       'title': "Layer 1 Heading 1",
                       'text': "Layer 1, first text.",
                       'children': []},
                      {'short_title': "Layer_1b",
                       'title': "Layer 1 Heading 2",
                       'text': "Layer 1, second text.",
                       'children': []},
                  ]}
        create_structure_from_structure_node_schema(schema,self.slot1,[self.hugo])
        node_list = Node.objects.filter(title="My first structure Node").all()
        self.assertEqual(len(node_list),1)
        n = node_list[0]
        self.assertEqual(n.text.text,"This is the text.")
        slots = n.children.all()
        self.assertEqual(len(slots),2)
        self.assertEqual(slots[0].title, "Layer_1a")
        self.assertEqual(slots[1].title, "Layer_1b")
        self.assertEqual(len(slots[0].children.all()),1)
        sub_structure1 = slots[0].children.all()[0]
        self.assertEqual(sub_structure1.title, "Layer 1 Heading 1")
        self.assertEqual(sub_structure1.text.text, "Layer 1, first text.")
        self.assertEqual(len(sub_structure1.children.all()),0)
        self.assertEqual(len(slots[1].children.all()),1)
        sub_structure1 = slots[1].children.all()[0]
        self.assertEqual(sub_structure1.title, "Layer 1 Heading 2")
        self.assertEqual(sub_structure1.text.text, "Layer 1, second text.")
        self.assertEqual(len(sub_structure1.children.all()),0)


