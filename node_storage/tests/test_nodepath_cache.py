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
from ..models import PathCache, Node
from node_storage.factory import create_slot, create_structureNode, create_argument
from node_storage.path_helpers import get_root_node


class NodePathCacheTest(TestCase):
    def setUp(self):
        self.root = get_root_node()

    def test_root_node_has_path(self):
        r = PathCache.objects.get(path='').node
        self.assertEqual(r, self.root)

        p = PathCache.objects.get(node=self.root).path
        self.assertEqual(p, '')

    def test_append_child_slot_adds_to_path_cache(self):
        slot = create_slot('Foo')
        self.root.append_child(slot)
        self.assertEqual(slot, PathCache.objects.get(path='Foo').node)
        self.assertEqual('Foo', PathCache.objects.get(node=slot).path)

    def test_append_child_structure_node_adds_to_path_cache(self):
        slot = create_slot('Foo')
        self.root.append_child(slot)
        sn = create_structureNode("Foobarbaz")
        slot.append_child(sn)

        self.assertEqual(sn, PathCache.objects.get(path='Foo.1').node)
        self.assertEqual('Foo.1', PathCache.objects.get(node=sn).path)

    def test_append_child_slot_adds_all_paths(self):
        slot = create_slot('Foo')
        self.root.append_child(slot)
        sn1 = create_structureNode("Foobarbaz1")
        slot.append_child(sn1)
        sn2 = create_structureNode("Foobarbaz2")
        slot.append_child(sn2)
        slot_t = create_slot('Ba')
        sn1.append_child(slot_t)
        sn2.append_child(slot_t)

        sn_test = create_structureNode("Barbaren")
        slot_t.append_child(sn_test)

        self.assertEqual(sn_test, PathCache.objects.get(path='Foo.1/Ba.1').node)
        self.assertEqual(sn_test, PathCache.objects.get(path='Foo.2/Ba.1').node)

    def test_creating_an_argument_adds_to_path_cache(self):
        slot = create_slot('Foo')
        self.root.append_child(slot)
        sn = create_structureNode("Foobarbaz1")
        slot.append_child(sn)

        a = create_argument(sn, arg_type='con')
        node_a = Node.objects.get(id=a.id)
        self.assertEqual(node_a, PathCache.objects.get(path='Foo.1.con.1').node)
