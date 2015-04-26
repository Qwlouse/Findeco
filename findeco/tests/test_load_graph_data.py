#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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
#endregion #####################################################################

from django.test import TestCase
from django.core.urlresolvers import reverse
import json
from findeco.jsonvalidator import json_decode
from findeco.view_helpers import create_graph_data_node_for_structure_node
from node_storage.path_helpers import get_root_node
from node_storage.factory import create_user, create_slot, create_structureNode
from node_storage.factory import create_textNode


class LoadGraphDataTest(TestCase):
    def setUp(self):
        self.max = create_user('max')
        self.root = get_root_node()
        self.bla = create_slot("Bla")
        self.root.append_child(self.bla)
        self.bla1 = create_structureNode('Bla ist Bla',
                                         "Das musste gesagt werden.",
                                         [self.max])
        self.bla.append_child(self.bla1)
        self.blubb = create_slot("Blubb")
        self.bla1.append_child(self.blubb)
        self.blubb1 = create_textNode("Blubb ist eins", "Gesagt ist gedacht.",
                                      [self.max])
        self.blubb.append_child(self.blubb1)
        self.blubb2 = create_textNode("Blubb die Zweite",
                                      "Geschrieben ist notiert.", [self.max])
        self.blubb.append_child(self.blubb2)
        self.blubb2d = create_textNode("Blubb die Zweite",
                                       "Geschrieben ist anders notiert.",
                                       [self.max])
        self.blubb.append_child(self.blubb2d)
        self.blubb2.add_derivate(self.blubb2d)
        self.bla2 = create_textNode("Follopp", "Globbern!", [self.max])
        self.bla.append_child(self.bla2)
        self.bla2.add_derivate(self.blubb2)
        self.bla3 = create_textNode("Folloppiii", "Globbern! Den ganzen Tag.",
                                    [self.max])
        self.bla.append_child(self.bla3)
        self.blubb2.add_derivate(self.bla3)
        self.bla4 = create_textNode("Flop", "Glob!", [self.max])
        self.bla.append_child(self.bla4)
        self.bla3.add_derivate(self.bla4)

    def test_root_node(self):
        response = self.client.get(
            reverse('load_graph_data',
                    kwargs=dict(path='', graph_data_type='withSpam')))
        parsed = json_decode(response.content)
        self.assertTrue('loadGraphDataResponse' in parsed)
        self.assertTrue('graphDataChildren' in parsed['loadGraphDataResponse'])
        self.assertTrue('graphDataRelated' in parsed['loadGraphDataResponse'])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataRelated'],
                         [])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataChildren'],
                         [create_graph_data_node_for_structure_node(self.root)])

    def test_paths(self):
        response = self.client.get(
            reverse('load_graph_data',
                    kwargs=dict(path='Bla.1/Blubb.2',
                                graph_data_type='withSpam')))
        parsed = json_decode(response.content)

        # self.assertEqual(parsed['loadGraphDataResponse']['graphDataRelated'],
        #                  [create_graph_data_node_for_structure_node(self.bla2),
        #                   create_graph_data_node_for_structure_node(self.bla3)])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataChildren'],
                         [create_graph_data_node_for_structure_node(
                             self.blubb1),
                          create_graph_data_node_for_structure_node(
                              self.blubb2),
                          create_graph_data_node_for_structure_node(
                              self.blubb2d)])

        response = self.client.get(
            reverse('load_graph_data',
                    kwargs=dict(path='Bla.4', graph_data_type='withSpam')))
        parsed = json_decode(response.content)
        # self.assertEqual(parsed['loadGraphDataResponse']['graphDataRelated'],
        #                  [create_graph_data_node_for_structure_node(
        #                      self.blubb2)])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataChildren'],
                         [create_graph_data_node_for_structure_node(self.bla1),
                          create_graph_data_node_for_structure_node(self.bla2),
                          create_graph_data_node_for_structure_node(self.bla3),
                          create_graph_data_node_for_structure_node(self.bla4)])