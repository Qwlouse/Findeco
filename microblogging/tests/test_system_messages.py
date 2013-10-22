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
from node_storage.factory import create_user, create_nodes_for_path
from node_storage.path_helpers import get_root_node
from findeco.models import get_system_user
from microblogging.system_messages import post_node_was_flagged_message, post_node_was_unflagged_message
from microblogging.system_messages import post_new_derivate_for_node_message
from microblogging.models import Post


class ViewHelpersTest(TestCase):
    def test_post_node_was_flagged_message(self):
        hugo = create_user('Hugo')
        post = post_node_was_flagged_message('/', hugo)
        self.assertEqual(post.author, get_system_user())
        self.assertEqual(post.location, get_root_node())
        self.assertEqual(post.post_type, Post.SPAM_MARKED)
        self.assertIn(hugo, post.mentions.all())
        self.assertEqual(
            post.text_cache,
            '<span style="color: gray;">Hinweis:</span> ' +
            '<a href="/user/hugo">Hugo</a> hat <a href="/">/</a> als Spam markiert.')

    def test_post_node_was_unflagged_message(self):
        hugo = create_user('Hugo')
        post = post_node_was_unflagged_message('/', hugo)
        self.assertEqual(post.author, get_system_user())
        self.assertEqual(post.location, get_root_node())
        self.assertEqual(post.post_type, Post.SPAM_UNMARKED)
        self.assertIn(hugo, post.mentions.all())
        self.assertEqual(
            post.text_cache,
            '<span style="color: gray;">Hinweis:</span> ' +
            '<a href="/user/hugo">Hugo</a> hat die Spam-Markierung für <a href="/">/</a> entfernt.')

    def test_post_new_derivate_for_node_message(self):
        hugo = create_user('Hugo')
        node_A = create_nodes_for_path('/bla.1/blubb.1', hugo)
        node_B = create_nodes_for_path('/bla.2/pling.1', hugo)
        post = post_new_derivate_for_node_message(hugo, '/bla.1/blubb.1', '/bla.2/pling.1')
        self.assertEqual(post.author, get_system_user())
        self.assertEqual(post.location, node_A)
        self.assertEqual(post.post_type, Post.NODE_REFINED)
        self.assertIn(hugo, post.mentions.all())
        self.assertIn(node_A, post.node_references.all())
        self.assertIn(node_B, post.node_references.all())
        self.assertEqual(post.node_references.count(), 2)
        self.assertEqual(
            post.text_cache,
            '<span style="color: gray;">Hinweis:</span> ' +
            '<a href="/user/hugo">Hugo</a> hat <a href="/bla.1/blubb.1">blubb_long</a> zu ' +
            '<a href="/bla.2/pling.1">pling_long</a> weiterentwickelt.')