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
from microblogging.factory import create_post
from node_storage.factory import create_user, create_nodes_for_path
from microblogging.models import Post


class PostTest(TestCase):

    def setUp(self):
        self.hugo = create_user('hugo')
        self.herbert = create_user('herbert')

        self.foo1 = create_nodes_for_path('foo.1')

        self.schema_skeleton = {
            'author': self.hugo.id,
            'location': self.foo1,
            'type': "userpost",
            'template_text': "some text",
            'mentions': [],
            'references': [],
            'answer_to': None
        }

    def test_render_text_generates_text(self):
        schema = self.schema_skeleton
        schema['template_text'] = "text without special stuff"
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, "text without special stuff")

    def test_render_text_inserts_users(self):
        schema = self.schema_skeleton
        schema['template_text'] = "reference users {u0}, {u1} and {u0} again."
        schema['mentions'] = [self.hugo, self.herbert]
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, 'reference users '
                                       '<a href="/user/hugo">@hugo</a>, '
                                       '<a href="/user/herbert">@herbert</a> '
                                       'and <a href="/user/hugo">@hugo</a> '
                                       'again.')

    def test_create_post_adds_many_to_many_relations(self):
        node2 = create_nodes_for_path('bar.1')
        schema = self.schema_skeleton
        schema['template_text'] = "reference to {u0} and {u1} and {n0} and {n1}"
        schema['mentions'] = [self.hugo, self.herbert]
        schema['references'] = [self.foo1, node2]
        p = create_post(schema)
        p_db = Post.objects.all()[0]
        self.assertEqual(p.author, p_db.author)
        self.assertEqual(p.post_type, p_db.post_type)
        self.assertListEqual(list(p.mentions.all()), list(p_db.mentions.all()))
        self.assertListEqual(list(p.node_references.all()), list(p_db.node_references.all()))

