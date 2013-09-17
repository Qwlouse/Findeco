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
        self.foo1bar1 = create_nodes_for_path('foo.1/bar.1')

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

    def test_render_text_escapes_html(self):
        schema = self.schema_skeleton
        schema['template_text'] = "<script> evil </script>"
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, "&lt;script&gt; evil &lt;/script&gt;")

    def test_render_text_inserts_mentions(self):
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

    def test_render_text_inserts_node_references(self):
        schema = self.schema_skeleton
        schema['template_text'] = "reference nodes {n0}, {n1} and {n0} again."
        schema['references'] = [self.foo1, self.foo1bar1]
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, 'reference nodes '
                                       '<a href="/foo.1">foo_long</a>, '
                                       '<a href="/foo.1/bar.1">bar_long</a> '
                                       'and <a href="/foo.1">foo_long</a> '
                                       'again.')

    def test_render_text_inserts_links_for_hash_tags(self):
        schema = self.schema_skeleton
        schema['template_text'] = "link to #hash #tag"
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, 'link to '
                                       '<a href="/search/hash">#hash</a> '
                                       '<a href="/search/tag">#tag</a>')

    def test_render_text_converts_links(self):
        schema = self.schema_skeleton
        schema['template_text'] = "link to http://www.findeco.de"
        p = create_post(schema)
        p.render()
        self.assertEqual(p.text_cache, 'link to '
                                       '<a href="http://www.findeco.de">'
                                       'http://www.findeco.de</a>')

