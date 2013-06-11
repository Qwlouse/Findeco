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
from node_storage import Text, Node, Argument, TextCache, IndexCache
from node_storage.factory import create_slot, create_structureNode, create_vote, create_user, create_spam_flag, create_argument
from node_storage.models import PathCache
from node_storage.tools import delete_node
from node_storage.path_helpers import get_root_node, get_node_for_path, IllegalPath


class ToolsTest(TestCase):
    def setUp(self):
        self.horst = create_user('horst')
        self.udo = create_user('udo')

        self.root = get_root_node()
        self.slot1 = create_slot('soon_empty')
        self.root.append_child(self.slot1)
        self.node = create_structureNode('To be or not to be', 'never both')
        self.slot1.append_child(self.node)
        self.arg = create_argument(self.node, 'c', "no", "lyrics")
        self.path = 'soon_empty.1'
        TextCache.objects.create(path=self.path, paragraphs="doesn't matter")
        IndexCache.objects.create(path=self.path, index_nodes="doesn't matter")

        self.slot2 = create_slot('verfassungswiedrig')
        self.root.append_child(self.slot2)
        self.source = create_structureNode('BöserTitel', 'gewöhnlicher text')
        self.slot2.append_child(self.source)
        self.derivate = create_structureNode('BöserTitel', 'verfassungswiedriger text')
        self.slot2.append_child(self.derivate)
        self.source.add_derivate(self.derivate, arg_type='con', title="zu schwach",
                                 text="muss fieser werden", authors=[self.udo])

        self.source_path = 'verfassungswiedrig.1'
        self.derivate_path = 'verfassungswiedrig.2'

        create_vote(self.udo, [self.node])
        create_vote(self.horst, [self.source, self.node])
        create_spam_flag(self.horst, [self.node])

    def test_delete_node_removes_node(self):
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertRaises(IllegalPath, get_node_for_path, self.path)

    def test_delete_node_removes_votes(self):
        self.assertEqual(self.udo.vote_set.count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(self.udo.vote_set.count(), 0)

    def test_delete_node_removes_spam_flags(self):
        self.assertEqual(self.horst.spamflag_set.count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(self.horst.spamflag_set.count(), 0)

    def test_delete_node_does_not_remove_vote_from_source(self):
        self.assertEqual(self.source.votes.count(), 1)
        node = get_node_for_path(self.derivate_path)
        delete_node(node)
        self.assertEqual(self.source.votes.count(), 1)

    def test_delete_node_removes_text(self):
        self.assertEqual(Text.objects.filter(text='never both').count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(Text.objects.filter(text='never both').count(), 0)

    def test_delete_node_removes_derivation(self):
        self.assertEqual(self.source.derivates.count(), 1)
        node = get_node_for_path(self.derivate_path)
        delete_node(node)
        self.assertEqual(self.source.derivates.count(), 0)

    def test_delete_node_removes_empty_parent_slot(self):
        self.assertEqual(Node.objects.filter(title='soon_empty').count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(Node.objects.filter(title='soon_empty').count(), 0)

    def test_delete_node_removes_derivates(self):
        self.assertEqual(Node.objects.filter(title='BöserTitel').count(), 2)
        node = get_node_for_path(self.source_path)
        delete_node(node)
        self.assertEqual(Node.objects.filter(title='BöserTitel').count(), 0)

    def test_delete_node_removes_argument(self):
        self.assertEqual(Argument.objects.filter(title='no').count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(Argument.objects.filter(title='no').count(), 0)

    def test_delete_node_on_derivate_removes_derivation_argument(self):
        self.assertEqual(Argument.objects.filter(title='zu schwach').count(), 1)
        node = get_node_for_path(self.derivate_path)
        delete_node(node)
        self.assertEqual(Argument.objects.filter(title='zu schwach').count(), 0)

    def test_delete_node_removes_path_cache_entry(self):
        self.assertEqual(PathCache.objects.filter(path=self.path).count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(PathCache.objects.filter(path=self.path).count(), 0)

    def test_delete_node_removes_text_cache_entry(self):
        self.assertEqual(TextCache.objects.filter(path=self.path).count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(TextCache.objects.filter(path=self.path).count(), 0)

    def test_delete_node_removes_index_cache_entry(self):
        self.assertEqual(IndexCache.objects.filter(path=self.path).count(), 1)
        node = get_node_for_path(self.path)
        delete_node(node)
        self.assertEqual(IndexCache.objects.filter(path=self.path).count(), 0)