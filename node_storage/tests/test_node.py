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
from node_storage import Node, get_root_node
from node_storage.factory import create_structureNode, create_user, create_vote, create_argument
from node_storage.models import NodeOrder, Derivation

class NodeTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hans = create_user('hans')
        self.hugo = create_user('hugo')

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

    def test_add_derivate(self):
        n = create_structureNode("Source", authors=[self.hans])
        d = create_structureNode("Derivate", authors=[self.hans])
        a = create_argument()
        n.add_derivate(a, d)


        self.assertIn(d, n.derivates.all())
        self.assertIn(n, d.sources.all())

        no = Derivation.objects.filter(source=n, derivate=d)
        self.assertTrue(no.count() == 1)
        self.assertEqual(no[0].argument, a)

        self.assertIn(no[0], n.derivative_order_set.all())
        self.assertIn(no[0], d.source_order_set.all())

    def test_get_unfollows_on_node_without_sources_returns_0(self):
        self.assertEqual(self.root.get_unfollows(), 0)

    def test_get_unfollows_on_node_with_same_votes_than_source_returns_0(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n, n2])
        create_vote(self.hugo, [n, n2])
        self.assertEqual(n2.get_unfollows(), 0)

    def test_get_unfollows_with_an_unfollow_returns_1(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n])
        create_vote(self.hugo, [n, n2])
        self.assertEqual(n2.get_unfollows(), 1)

    def test_get_unfollows_with_2_unfollows_returns_2(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n])
        create_vote(self.hugo, [n])
        self.assertEqual(n2.get_unfollows(), 2)

    def test_get_unfollows_counts_votes_from_multiple_sources_only_once(self):
        n1 = create_structureNode('Foo1')
        n2 = create_structureNode('Foo2')
        d = create_structureNode('Foo12')
        n1.add_derivate(create_argument(), d)
        n2.add_derivate(create_argument(), d)
        create_vote(self.hans, [n1, n2])
        self.assertEqual(d.get_unfollows(), 1)

    def test_get_unfollows_does_count_users_and_not_votes(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n])
        create_vote(self.hans, [n2])
        self.assertEqual(n2.get_unfollows(), 0)

    def test_get_newfollows_on_node_without_votes_or_sources_returns_0(self):
        self.assertEqual(self.root.get_newfollows(), 0)

    def test_get_newfollows_on_node_without_sources_returns_number_of_follows(self):
        n = create_structureNode('Foo')
        create_vote(self.hans, [n])
        create_vote(self.hugo, [n])
        self.assertEqual(n.get_newfollows(), 2)

    def test_get_newfollows_on_node_with_same_votes_than_source_returns_0(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n, n2])
        create_vote(self.hugo, [n, n2])
        self.assertEqual(n2.get_newfollows(), 0)

    def test_get_newfollows_with_a_newfollow_returns_1(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n2])
        create_vote(self.hugo, [n, n2])
        self.assertEqual(n2.get_newfollows(), 1)

    def test_get_newfollows_with_2_newfollows_returns_2(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n2])
        create_vote(self.hugo, [n2])
        self.assertEqual(n2.get_newfollows(), 2)

    def test_get_newfollows_does_count_votes_and_not_users(self):
        n = create_structureNode('Foo')
        n2 = create_structureNode('Foo2')
        n.add_derivate(create_argument(), n2)
        create_vote(self.hans, [n])
        create_vote(self.hans, [n2])
        self.assertEqual(n2.get_newfollows(), 1)