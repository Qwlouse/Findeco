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
from node_storage import Node
from node_storage.models import NodeOrder


class NodeTest(TestCase):
    def test_node_constructable(self):
        n = Node()
        n.node_type = "structureNode"
        n.save()
        self.assertEqual(n.node_type, "structureNode")

    def test_node_append_child(self):
        n = Node()
        n.save()
        c = Node()
        c.save()
        n.append_child(c)

        self.assertIn(c, n.children.all())
        self.assertIn(n, c.parents.all())

        no = NodeOrder.objects.filter(parent=n, child=c)
        self.assertTrue(no.count() == 1)
        self.assertEqual(no[0].position, 1)

        self.assertIn(no[0], n.child_order_set.all())
        self.assertIn(no[0], c.parent_order_set.all())

    def test_node(self):
        pass