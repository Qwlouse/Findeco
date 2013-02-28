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
from ..models import PathCache
from node_storage.factory import create_slot
from node_storage.path_helpers import get_root_node


class NodePathCacheTest(TestCase):
    def setUp(self):
        self.root = get_root_node()

    def test_root_node_has_path(self):
        r = PathCache.objects.get(path='').node
        self.assertEqual(r, self.root)

        p = PathCache.objects.get(node=self.root).path
        self.assertEqual(p, '')

    def test_append_child_adds_to_path_cache(self):
        slot = create_slot('Foo')
        self.root.append_child(slot)
        self.assertEqual(slot, PathCache.objects.get(path='Foo').node)
        self.assertEqual('Foo', PathCache.objects.get(node=slot).path)