#!/usr/bin/python
# coding=utf-8
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
################################################################################
from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
import json
from findeco.view_helpers import create_graph_data_node_for_structure_node
from node_storage import get_root_node

class LoadGraphDataTest(TestCase):
    def setUp(self):
        self.root = get_root_node()

    def test_root_node(self):
        response = self.client.get(reverse('load_graph_data', kwargs=dict(path='', graph_data_type='withSpam')))
        parsed = json.loads(response.content)
        self.assertTrue('loadGraphDataResponse' in parsed)
        self.assertTrue('graphDataChildren' in parsed['loadGraphDataResponse'])
        self.assertTrue('graphDataRelated' in parsed['loadGraphDataResponse'])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataRelated'],[])
        self.assertEqual(parsed['loadGraphDataResponse']['graphDataChildren'],
            [create_graph_data_node_for_structure_node(self.root)])