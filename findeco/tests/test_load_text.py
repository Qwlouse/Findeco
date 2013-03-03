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
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.test import TestCase
import json
from findeco.tests.helpers import assert_is_error_response

from node_storage import get_root_node
from node_storage.factory import create_slot, create_user, create_textNode
from node_storage.factory import create_vote, create_structureNode
from node_storage.factory import create_argument
from ..api_validation import errorResponseValidator


class LoadTextTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

        self.root = get_root_node()
        self.slot1 = create_slot('Wahlprogramm')
        self.root.append_child(self.slot1)
        self.structureNode1 = create_structureNode(
            'LangerWahlprogrammTitel',
            text="Einleitungstext",
            authors=[self.hans])
        self.slot1.append_child(self.structureNode1)
        self.slot11 = create_slot('Transparenz')
        self.structureNode1.append_child(self.slot11)
        self.structureNode11 = create_structureNode(
            'Traaaansparenz',
            text="Transparenz ist wichtig.",
            authors=[self.hans])
        self.slot11.append_child(self.structureNode11)
        self.slot111 = create_slot('Ebene_3')
        self.structureNode11.append_child(self.slot111)
        self.structureNode111 = create_structureNode(
            'Eeeebeneee 3',
            authors=[self.hans])
        self.slot111.append_child(self.structureNode111)
        self.slot1111 = create_slot('Ebene_4')
        self.structureNode111.append_child(self.slot1111)
        self.structureNode1111 = create_structureNode(
            'Eeeebeneee 4',
            authors=[self.hans])
        self.slot1111.append_child(self.structureNode1111)
        self.slot11111 = create_slot('Ebene_5')
        self.structureNode1111.append_child(self.slot11111)
        self.structureNode11111 = create_structureNode(
            'Eeeebeneee 5',
            authors=[self.hans])
        self.slot11111.append_child(self.structureNode11111)
        self.slot111111 = create_slot('Ebene_6')
        self.structureNode11111.append_child(self.slot111111)
        self.structureNode111111 = create_structureNode(
            'Eeeebeneee 6',
            authors=[self.hans])
        self.slot111111.append_child(self.structureNode111111)
        self.slot1111111 = create_slot('Ebene_7')
        self.structureNode111111.append_child(self.slot1111111)
        self.textnode1111111 = create_textNode(
            'Traaaansparenz',
            text="Auf Ebene 7.",
            authors=[self.hans])
        self.slot1111111.append_child(self.textnode1111111)
        self.slot12 = create_slot('Bildung')
        self.structureNode1.append_child(self.slot12)
        self.textnode12 = create_textNode(
            'Biiildung',
            authors=[self.hans])
        self.slot12.append_child(self.textnode12)
        self.slot13 = create_slot('Datenschutz')
        self.structureNode1.append_child(self.slot13)
        self.textnode13 = create_textNode(
            'Daaatenschutz', text="Blubb.", authors=[self.hans])
        self.slot13.append_child(self.textnode13)
        self.textnode13_a1 = create_argument(
            self.textnode13, arg_type='con', title='Dagegen',
            text="...denn ihr seid dafür", authors=[self.hugo])

        self.slot2 = create_slot('Grundsatzprogramm')
        self.root.append_child(self.slot2)
        self.textnode2 = create_textNode(
            'LangerGrundsatzTitel', authors=[self.hugo])
        self.slot2.append_child(self.textnode2)

        self.slot3 = create_slot('Organisatorisches')
        self.root.append_child(self.slot3)
        self.textnode31 = create_textNode('Langweilig1', authors=[self.hans])
        self.textnode32 = create_textNode('Langweilig2', authors=[self.hugo])
        self.textnode33 = create_textNode(
            'Langweilig3', authors=[self.hans, self.hugo])
        self.slot3.append_child(self.textnode31)
        self.slot3.append_child(self.textnode32)
        self.slot3.append_child(self.textnode33)
        create_vote(self.hans, [self.textnode33])

        self.top_slots = [self.slot1, self.slot2, self.slot3]
        self.child_slots = [self.slot11, self.slot12, self.slot13]
        self.short_titles = ['Wahlprogramm', 'Grundsatzprogramm',
                             'Organisatorisches']
        self.full_titles = ['LangerWahlprogrammTitel', 'LangerGrundsatzTitel',
                            'Langweilig3']
        self.authors = [[self.hans], [self.hugo], [self.hans, self.hugo]]
        self.maxDiff = None

    def test_textnode_gives_correct_text(self):
        response = self.client.get(
            reverse('load_text',
                    kwargs=dict(path="Wahlprogramm.1/Datenschutz.1")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['loadTextResponse']['paragraphs'][0]['wikiText'],
                         "= Daaatenschutz =\nBlubb.")

    def test_structurenode_gives_correct_text(self):
        response = self.client.get(
            reverse('load_text', kwargs=dict(path="Wahlprogramm.1")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['loadTextResponse']['paragraphs'][0]['wikiText'],
                         "= LangerWahlprogrammTitel =\nEinleitungstext")
        self.assertEqual(data['loadTextResponse']['paragraphs'][0]['path'],
                         "Wahlprogramm.1")

        expected_text = """== [[#/Wahlprogramm.1/Transparenz.1|Traaaansparenz]] ==
Transparenz ist wichtig.

=== [[#/Wahlprogramm.1/Transparenz.1/Ebene_3.1|Eeeebeneee 3]] ===


==== [[#/Wahlprogramm.1/Transparenz.1/Ebene_3.1/Ebene_4.1|Eeeebeneee 4]] ====


===== [[#/Wahlprogramm.1/Transparenz.1/Ebene_3.1/Ebene_4.1/Ebene_5.1|Eeeebeneee 5]] =====


====== [[#/Wahlprogramm.1/Transparenz.1/Ebene_3.1/Ebene_4.1/Ebene_5.1/Ebene_6.1|Eeeebeneee 6]] ======


====== [[#/Wahlprogramm.1/Transparenz.1/Ebene_3.1/Ebene_4.1/Ebene_5.1/Ebene_6.1/Ebene_7.1|Traaaansparenz]] ======
Auf Ebene 7."""
        self.assertEqual(data['loadTextResponse']['paragraphs'][1]['wikiText'],
                         expected_text)
        self.assertEqual(data['loadTextResponse']['paragraphs'][1]['path'],
                         "Wahlprogramm.1/Transparenz.1")
        self.assertEqual(data['loadTextResponse']['paragraphs'][2]['wikiText'],
                         "== [[#/Wahlprogramm.1/Bildung.1|Biiildung]] ==\n")
        self.assertEqual(data['loadTextResponse']['paragraphs'][2]['path'],
                         "Wahlprogramm.1/Bildung.1")
        self.assertEqual(data['loadTextResponse']['paragraphs'][3]['wikiText'],
                         "== [[#/Wahlprogramm.1/Datenschutz.1|Daaatenschutz]] ==\nBlubb.")
        self.assertEqual(data['loadTextResponse']['paragraphs'][3]['path'],
                         "Wahlprogramm.1/Datenschutz.1")

    def test_load_text_on_argument_gives_argument_text(self):
        response = self.client.get(
            reverse('load_text',
                    kwargs=dict(path="Wahlprogramm.1/Datenschutz.1.con.1")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expected_response = {
            'loadTextResponse': {
                'paragraphs': [{
                    'wikiText':"= Dagegen =\n...denn ihr seid dafür",
                    'path':"Wahlprogramm.1/Datenschutz.1.con.1",
                    'isFollowing':0,
                    'isFlagging':0,
                    'authorGroup': [{
                        'displayName':"hugo",
                        'description':"",
                        'followers':[],
                        'followees':[]
                    }]
                }],
                'isFollowing': 0,
                'isFlagging': 0
            }
        }
        self.assertEqual(data, expected_response)

    def test_multiple_loads_give_same_text(self):
        url = reverse('load_text',
                      kwargs=dict(path="Wahlprogramm.1/Datenschutz.1"))
        response = self.client.get(url)
        data_first = json.loads(response.content)
        for i in range(3):
            response = self.client.get(url)
            data = json.loads(response.content)
            self.assertEqual(data, data_first)

    def test_on_illegal_path_gives_error_response(self):
        illegal_paths = ['Wahlprogramm.1/foo',
                         'Wahlprogramm.1/foo.1.pro']
        for p in illegal_paths:
            response = self.client.get(
                reverse('load_text', kwargs=dict(path=p)))
            assert_is_error_response(response, "IllegalPath")