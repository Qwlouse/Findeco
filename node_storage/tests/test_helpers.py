#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
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
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from ..path_helpers import get_favorite_if_slot
from ..models import Node, NodeOrder

def setup():
    root = Node()
    root.node_type = 'structureNode'
    root.save()
    slot1 = Node()
    slot1.node_type = 'slot'
    slot1.save()
    slot1_order = NodeOrder()
    slot1_order.parent = root
    slot1_order.child = slot1
    slot1_order.position = 0
    slot1_order.save()
    text1 = Node()
    text1.node_type = 'textNode'
    text1.save()
    text1_order = NodeOrder()
    text1_order.parent = slot1
    text1_order.child = text1
    text1_order.position = 1
    text1_order.save()
    slot2 = Node()
    slot2.node_type = 'slot'
    slot2.save()
    slot2_order = NodeOrder()
    slot2_order.parent = root
    slot2_order.child = slot2
    slot2_order.position = 1
    slot2_order.save()
    return root, slot1, text1

class HelpersTest(TestCase):
    def test_get_favorite_if_slot(self):
        """
        bla
        """
        root, slot1, text1 = setup()
        n = get_favorite_if_slot(root)
        self.assertEqual(n, root)
        n = get_favorite_if_slot(slot1)
        self.assertEqual(n, text1)
        n = get_favorite_if_slot(text1)
        self.assertEqual(n, text1)
