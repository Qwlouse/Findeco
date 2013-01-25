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
from django.test import TestCase
from node_storage.structure_parser import validate_structure_schema, InvalidWikiStructure
from ..structure_parser import strip_accents, substitute_umlauts, parse
from ..structure_parser import remove_unallowed_chars, turn_into_valid_short_title, getHeadingMatcher
from ..structure_parser import create_structure_from_structure_node_schema
from ..factory import create_user, create_slot, create_structureNode, create_textNode, create_argument
from ..path_helpers import get_root_node
from ..models import Node
import re

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
            ("schöner Titel was?", "schoener_Titel_was", ["schoener_Titel_was", "schoener_Titel_was1"],
             "schoener_Titel_was2"),
            ("viiiiiieeeeeel zuuuuuuu laaaaaaaang", "viiiiiieeeeeel_zuuuu",
             ["viiiiiieeeeeel_zuuuu", "viiiiiieeeeeel_zuuu1", "viiiiiieeeeeel_zuuu2", "viiiiiieeeeeel_zuuu3",
              "viiiiiieeeeeel_zuuu4", "viiiiiieeeeeel_zuuu5", "viiiiiieeeeeel_zuuu6", "viiiiiieeeeeel_zuuu7",
              "viiiiiieeeeeel_zuuu8", "viiiiiieeeeeel_zuuu9"], "viiiiiieeeeeel_zuu10"),
            ("viel )()()(()()( zu {}{}{}{ lang", "viel_zu_lang", ["viel_zu_lang"], "viel_zu_lang1"),
            ("", "1", ["1", "2", "3"], "4"),
            ("N0body is as L€€+.a$.m3", "N0body_is_as_Lam3", ["N0body_is_as_Lam3"], "N0body_is_as_Lam31")
        ]
        for t, st, _, _ in titles:
            self.assertEqual(turn_into_valid_short_title(t), st)
        for t, _, st_set, st in titles:
            self.assertEqual(turn_into_valid_short_title(t, set(st_set)), st)

    def test_getHeadingMatcher(self):
        s = "1, 6"
        self.assertEqual(getHeadingMatcher(level=0),re.compile(r"^\s*={%s}(?P<title>[^=§]+)(?:§\s*(?P<short_title>[^=§\s]+)\s*)?=*\s*$"%s, flags=re.MULTILINE))
        for level in range(1,7):
            s = "%d"%level
            self.assertEqual(getHeadingMatcher(level=level),re.compile(r"^\s*={%s}(?P<title>[^=§]+)(?:§\s*(?P<short_title>[^=§\s]+)\s*)?=*\s*$"%s, flags=re.MULTILINE))
        self.assertRaises(ValueError,getHeadingMatcher,level=7)

    def test_validate_structure_schema_on_simple_example_with_slot(self):
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
        wiki = """
        = Titel =
        einleitungstext
        === slot1 ===
        text
        == Toller Slot § slot2 ==
        mehr text
        """
        self.assertRaises(InvalidWikiStructure,parse,wiki,"foo")
        wiki = "== Titel =="
        self.assertRaises(InvalidWikiStructure,parse,wiki,"foo")

class CreateStructureFromStructureNodeSchemaTest(TestCase):
    def setUp(self):
        self.hugo = create_user("Hugo")
        self.root = get_root_node()
        self.slot1 = create_slot("Slot_1")
        self.root.append_child(self.slot1)
        self.structure1 = create_structureNode("Layer 1","text",[self.hugo])
        self.slot1.append_child(self.structure1)
        self.slot11 = create_slot("SubSlot1")
        self.structure1.append_child(self.slot11)
        self.text1 = create_textNode("Layer 2","Layer 2 text.",[self.hugo])
        self.slot11.append_child(self.text1)
        self.slot12 = create_slot("SubSlot2")
        self.structure1.append_child(self.slot12)
        self.text2 = create_textNode("Layer 2 second heading","Layer 2 text 2.",[self.hugo])
        self.slot12.append_child(self.text2)

    def test_create_structure_from_structure_node_schema_with_origin_group(self):
        schema = {'short_title': "Ignored",
                  'title': "Layer 1",
                  'text': "text",
                  'children': [
                      {'short_title': "SubSlot1",
                       'title': "Layer 2",
                       'text': "Layer 2 text.",
                       'children': []},
                      {'short_title': "SubSlot2",
                       'title': "Layer 2 second heading",
                       'text': "Layer 2 text 2.",
                       'children': []},
                  ]}
        create_structure_from_structure_node_schema(schema,self.slot1,[self.hugo],origin_group=[self.structure1],argument=create_argument())
        node_list = Node.objects.filter(title="Layer 1").all()
        self.assertEqual(len(node_list),1)
        n = node_list[0]
        self.assertEqual(n,self.structure1)
        self.assertEqual(n.text.text,"text")
        slots = n.children.all()
        self.assertEqual(len(slots),2)
        self.assertEqual(slots[0],self.slot11)
        self.assertEqual(slots[0].title, "SubSlot1")
        self.assertEqual(slots[1],self.slot12)
        self.assertEqual(slots[1].title, "SubSlot2")
        self.assertEqual(len(slots[0].children.all()),1)
        sub_structure1 = slots[0].children.all()[0]
        self.assertEqual(sub_structure1,self.text1)
        self.assertEqual(sub_structure1.title, "Layer 2")
        self.assertEqual(sub_structure1.text.text, "Layer 2 text.")
        self.assertEqual(len(sub_structure1.children.all()),0)
        self.assertEqual(len(slots[1].children.all()),1)
        sub_structure2 = slots[1].children.all()[0]
        self.assertEqual(sub_structure2,self.text2)
        self.assertEqual(sub_structure2.title, "Layer 2 second heading")
        self.assertEqual(sub_structure2.text.text, "Layer 2 text 2.")
        self.assertEqual(len(sub_structure2.children.all()),0)

    def test_create_structure_from_structure_node_schema_with_origin_group_difference_in_second_layer(self):
        schema = {'short_title': "Ignored",
                  'title': "Layer 1",
                  'text': "text",
                  'children': [
                      {'short_title': "SubSlot1",
                       'title': "Layer 2",
                       'text': "Layer 2 text.",
                       'children': []},
                      {'short_title': "SubSlot2",
                       'title': "Layer 2 second heading",
                       'text': "Layer 2 text 2 but changed.",
                       'children': []},
                      ]}
        create_structure_from_structure_node_schema(schema,self.slot1,[self.hugo],origin_group=[self.structure1],argument=create_argument())
        node_list = Node.objects.filter(title="Layer 1").all()
        self.assertEqual(len(node_list),1)
        n = node_list[0]
        self.assertEqual(n,self.structure1)
        self.assertEqual(n.text.text,"text")
        slots = n.children.all()
        self.assertEqual(len(slots),2)
        self.assertEqual(slots[0],self.slot11)
        self.assertEqual(slots[0].title, "SubSlot1")
        self.assertEqual(slots[1],self.slot12)
        self.assertEqual(slots[1].title, "SubSlot2")
        self.assertEqual(len(slots[0].children.all()),1)
        sub_structure1 = slots[0].children.all()[0]
        self.assertEqual(sub_structure1,self.text1)
        self.assertEqual(sub_structure1.title, "Layer 2")
        self.assertEqual(sub_structure1.text.text, "Layer 2 text.")
        self.assertEqual(len(sub_structure1.children.all()),0)
        self.assertEqual(len(slots[1].children.all()),2)
        sub_structure2 = slots[1].children.all()[1]
        self.assertNotEqual(sub_structure2,self.text2)
        self.assertEqual(sub_structure2.title, "Layer 2 second heading")
        self.assertEqual(sub_structure2.text.text, "Layer 2 text 2 but changed.")
        self.assertEqual(len(sub_structure2.children.all()),0)
        self.assertEqual(sub_structure2.sources.all()[0],self.text2)

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
        sub_structure2 = slots[1].children.all()[0]
        self.assertEqual(sub_structure2.title, "Layer 1 Heading 2")
        self.assertEqual(sub_structure2.text.text, "Layer 1, second text.")
        self.assertEqual(len(sub_structure2.children.all()),0)


