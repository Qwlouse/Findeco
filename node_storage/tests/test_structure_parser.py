#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# #############################################################################
# Copyright (c) 2015 Klaus Greff <qwlouse@gmail.com>
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
# #############################################################################
#
# #############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from django.test import TestCase
from findeco.settings import STATICFILES_DIRS
from node_storage.structure_parser import validate_structure_schema
import os.path as path

from ..factory import create_slot, create_structureNode
from ..factory import create_textNode, create_user
from ..path_helpers import get_root_node
from ..models import Node
from ..structure_parser import create_structure_from_structure_node_schema
from ..structure_parser import InvalidWikiStructure
from ..structure_parser import parse as pyparser
from ..validation import remove_unallowed_chars
from ..validation import strip_accents
from ..validation import substitute_umlauts
from ..validation import turn_into_valid_short_title
import re

ESCAPABLE = re.compile(r'([^\x00-\x7f])')
HAS_UTF8 = re.compile(r'[\x80-\xff]')


def _js_escape_unicode_re_callack(match):
    s = match.group(0)
    n = ord(s)
    if n < 0x10000:
        return '\\u%04x' % (n,)
    else:
        # surrogate pair
        n -= 0x10000
        s1 = 0xd800 | ((n >> 10) & 0x3ff)
        s2 = 0xdc00 | (n & 0x3ff)
        return '\\u%04x\\u%04x' % (s1, s2)


def js_escape_unicode(s):
    """Return an ASCII-only representation of a JavaScript string"""
    if isinstance(s, str):
        if HAS_UTF8.search(s) is None:
            return s
        s = s.decode('utf-8')
    return str(ESCAPABLE.sub(_js_escape_unicode_re_callack, s))


class StructureParserTest(TestCase):
    def setUp(self):
        self.parse = pyparser

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
        self.assertEqual(
            remove_unallowed_chars("abc()[]{}<>?!.,:;+^`~|$#%def"),
            "abcdef")

    def test_remove_unallowde_chars_keeps_allowed_chars(self):
        valid = "abcdefghijklmnopqrstuvwxyz-1234567890" \
                "_ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertEqual(remove_unallowed_chars(valid), valid)

    def test_turn_into_valid_short_title(self):
        titles = [
            ("schöner Titel was?", "schoener_Titel_was",
             ["schoener_Titel_was", "schoener_Titel_was1"],
             "schoener_Titel_was2"),
            ("viiiiiieeeeeel zuuuuuuu laaaaaaaang", "viiiiiieeeeeel_zuuuu",
             ["viiiiiieeeeeel_zuuuu", "viiiiiieeeeeel_zuuu1",
              "viiiiiieeeeeel_zuuu2", "viiiiiieeeeeel_zuuu3",
              "viiiiiieeeeeel_zuuu4", "viiiiiieeeeeel_zuuu5",
              "viiiiiieeeeeel_zuuu6", "viiiiiieeeeeel_zuuu7",
              "viiiiiieeeeeel_zuuu8", "viiiiiieeeeeel_zuuu9"],
             "viiiiiieeeeeel_zuu10"),
            ("viel )()()(()()( zu {}{}{}{ lang", "viel_zu_lang",
             ["viel_zu_lang"], "viel_zu_lang1"),
            ("", "sub", ["sub", "sub1", "sub2"], "sub3"),
            ("N0body is as L€€+.a$.m3", "N0body_is_as_Lam3",
             ["N0body_is_as_Lam3"], "N0body_is_as_Lam31"),
            ("5 startswithnumber", "startswithnumber",
             ["startswithnumber"], "startswithnumber1")
        ]
        for t, st, _, _ in titles:
            self.assertEqual(turn_into_valid_short_title(t), st)
        for t, _, st_set, st in titles:
            self.assertEqual(turn_into_valid_short_title(t, set(st_set)), st)

    def test_validate_structure_schema_on_simple_example_with_slot(self):
        simple = dict(title="foo", short_title="foo", text="und bar und so",
                      children=[])
        self.assertTrue(validate_structure_schema(simple))

    def test_validate_structure_schema_on_simple_example(self):
        invalid = dict(title="foo", text="und bar und so", children=[])
        self.assertRaises(AssertionError, validate_structure_schema, invalid)

    def test_structure_parser_with_single_node_example(self):
        wiki = """=Titel=
        Der text."""
        schema = {
            'short_title': "foo",
            'title': "Titel",
            'text': "Der text.",
            'children': []
        }

        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    def test_structure_parser_processes_short_title(self):
        wiki = """=Titel=
        == Slot § shört, title!#$|~ ==
        """
        schema = {
            'short_title': "foo", 'title': "Titel", 'text': "",
            'children': [
                {'short_title': "shoert_title", 'title': "Slot", 'text': "",
                 'children': []
                 }
            ]
        }

        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    # TODO unskip this test
    # def test_structure_parser_turns_title_into_short_title(self):
    #     wiki = """=Titel=
    #     == ..::Very(!) long, slot title with special characters::..  ==
    #     """
    #     schema = {
    #         'short_title': "foo", 'title': "Titel", 'text': "",
    #         'children': [
    #             {'short_title': "Very_long_slot_title",
    #              'title': "..::Very(!) long, title with special characters::..",
    #              'text': "",
    #              'children': []
    #              }
    #         ]
    #     }
    #     for pname, parse in self.parser.items():
    #         s = parse(wiki, "foo")
    #         self.assertTrue(validate_structure_schema(s), "fail in " + pname)
    #         self.assertEqual(s, schema, "fail in " + pname)

    def test_structure_parser_with_single_node_example_strips_whitespace(self):
        wiki = """

        =  Titel   =


        Der text.


        """
        schema = {
            'short_title': "foo",
            'title': "Titel",
            'text': "Der text.",
            'children': []
        }
        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    def test_structure_parser_without_title_raises_exception(self):
        wiki = "nur text"
        self.assertRaises(InvalidWikiStructure, pyparser, wiki, "foo")

    def test_structure_parser_with_wrong_title_raises_exception(self):
        wiki = """
        == H2 titel ==
        dann text
        """
        self.assertRaises(InvalidWikiStructure, pyparser, wiki, "foo")

    def test_structure_parser_short_title_in_h1_is_silently_removed(self):
        wiki = """
        = Titel § removed =
        Der text.
        """
        schema = {
            'short_title': "foo",
            'title': "Titel",
            'text': "Der text.",
            'children': []
        }
        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    def test_structure_parser_with_nested_h2(self):
        wiki = """
        = Titel =
        einleitungstext
        == slot1 ==
        text
        == Toller Slot § slot2 ==
        mehr text
        """
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

        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    def test_structure_parser_with_nested_h4(self):
        wiki = """
        = Titel =
        einleitungstext
        ==== slot1 ====
        text
        ==== Toller Slot § slot2 ====
        mehr text
        """
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
        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)

    def test_structure_parser_with_deep_example(self):
        wiki = """
        = Titel =
        text
        == Titel1 § slot1 ==
        text1
        === Titel11 § slot11 ===
        text11
        ==== Titel111 § slot111 ===
        text111
        === Titel12 § slot12 ===
        text12
        == Titel2 § slot2 ==
        text2
        === Titel21 § slot21 ===
        text21
        === Titel22 § slot22 ===
        text22
        ==== Titel221 § slot221 ===
        text221
        """
        schema = {'title': "Titel", 'short_title': "foo", 'text': "text",
                  'children': [
                      {'title': "Titel1", 'short_title': "slot1",
                       'text': "text1",
                       'children': [
                           {'title': "Titel11", 'short_title': "slot11",
                            'text': "text11",
                            'children': [
                                {'title': "Titel111", 'short_title': "slot111",
                                 'text': "text111",
                                 'children': []}
                            ]},
                           {'title': "Titel12", 'short_title': "slot12",
                            'text': "text12",
                            'children': []},
                       ]},
                      {'title': "Titel2", 'short_title': "slot2",
                       'text': "text2",
                       'children': [
                           {'title': "Titel21", 'short_title': "slot21",
                            'text': "text21",
                            'children': []},
                           {'title': "Titel22", 'short_title': "slot22",
                            'text': "text22",
                            'children': [
                                {'title': "Titel221", 'short_title': "slot221",
                                 'text': "text221",
                                 'children': []}
                            ]},
                       ]},
                  ]}
        s = self.parse(wiki, "foo")
        self.assertTrue(validate_structure_schema(s))
        self.assertEqual(s, schema)


class CreateStructureFromStructureNodeSchemaTest(TestCase):
    def setUp(self):
        self.hugo = create_user("Hugo")
        self.root = get_root_node()
        self.slot1 = create_slot("Slot_1")
        self.root.append_child(self.slot1)
        self.structure1 = create_structureNode("Layer 1", "text", [self.hugo])
        self.slot1.append_child(self.structure1)
        self.slot11 = create_slot("SubSlot1")
        self.structure1.append_child(self.slot11)
        self.text1 = create_textNode("Layer 2", "Layer 2 text.", [self.hugo])
        self.slot11.append_child(self.text1)
        self.slot12 = create_slot("SubSlot2")
        self.structure1.append_child(self.slot12)
        self.text2 = create_textNode("Layer 2 second heading",
                                     "Layer 2 text 2.", [self.hugo])
        self.slot12.append_child(self.text2)

    def test_create_structure_from_structure_node_schema_without_origin_group(
            self):
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
        create_structure_from_structure_node_schema(schema, self.slot1,
                                                    self.hugo)
        node_list = Node.objects.filter(title="My first structure Node").all()
        self.assertEqual(len(node_list), 1)
        n = node_list[0]
        self.assertEqual(n.text.text, "This is the text.")
        slots = n.children.all()
        self.assertEqual(len(slots), 2)
        self.assertEqual(slots[0].title, "Layer_1a")
        self.assertEqual(slots[1].title, "Layer_1b")
        self.assertEqual(len(slots[0].children.all()), 1)
        sub_structure1 = slots[0].children.all()[0]
        self.assertEqual(sub_structure1.title, "Layer 1 Heading 1")
        self.assertEqual(sub_structure1.text.text, "Layer 1, first text.")
        self.assertEqual(len(sub_structure1.children.all()), 0)
        self.assertEqual(len(slots[1].children.all()), 1)
        sub_structure2 = slots[1].children.all()[0]
        self.assertEqual(sub_structure2.title, "Layer 1 Heading 2")
        self.assertEqual(sub_structure2.text.text, "Layer 1, second text.")
        self.assertEqual(len(sub_structure2.children.all()), 0)
