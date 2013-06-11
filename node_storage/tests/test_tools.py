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
from node_storage.factory import create_slot, create_structureNode, create_vote, create_user
from node_storage.tools import delete_node
from node_storage.path_helpers import get_root_node, get_node_for_path, IllegalPath


class ToolsTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.slot = create_slot('verfassungswiedrig')
        self.root.append_child(self.slot)
        self.node = create_structureNode('Auffälliger Titel', 'verfassungswiedriger text')
        self.slot.append_child(self.node)
        self.path = 'verfassungswiedrig.1'
        self.udo = create_user('udo')
        create_vote(self.udo, [self.node])


    def test_delete_node_removes_node(self):
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertRaises(IllegalPath, get_node_for_path, self.path)

    def test_delete_node_removes_votes(self):
        self.assertEqual(self.udo.vote_set.count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(self.udo.vote_set.count(), 0)

