#!/usr/bin/python
# coding=utf-8
# region License
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
#endregion #####################################################################
from __future__ import division, print_function, unicode_literals
from django.test import TestCase
from microblogging.factory import create_post
from microblogging.models import Post
from microblogging.tools import change_microblogging_authorship
from microblogging.tools import delete_posts_referring_to
from node_storage.factory import create_user, create_nodes_for_path


class ViewHelpersTest(TestCase):
    def test_change_microblogging_authorship_updates_author(self):
        hugo = create_user('hugo')
        create_user('herbert')
        arno = create_user('arno')

        post = create_post('hallo @hugo ich bins @herbert!', hugo)
        post.save()

        change_microblogging_authorship(hugo, arno)

        post = Post.objects.get(id=post.id)  # update object from DB

        self.assertEqual(post.author, arno)

    def test_change_microblogging_authorship_updates_mentions(self):
        hugo = create_user('hugo')
        create_user('herbert')
        arno = create_user('arno')

        post = create_post('hallo @hugo ich bins @herbert!', hugo)
        post.save()

        change_microblogging_authorship(hugo, arno)
        post = Post.objects.get(id=post.id)  # update object from DB

        self.assertNotIn(hugo, post.mentions.all())
        self.assertIn(arno, post.mentions.all())

    def test_change_microblogging_authorship_updates_template_text(self):
        hugo = create_user('hugo')
        create_user('herbert')
        arno = create_user('arno')

        post = create_post('hallo @hugo ich bins @herbert!', hugo)
        post.save()
        self.assertEqual(post.text_template, 'hallo {u0} ich bins {u1}!')
        change_microblogging_authorship(hugo, arno)
        post = Post.objects.get(id=post.id)  # update object from DB

        self.assertEqual(post.text_template, 'hallo {u1} ich bins {u0}!')

    def test_change_microblogging_authorship_can_deal_with_duplications(self):
        hugo = create_user('hugo')
        herbert = create_user('herbert')

        post = create_post('hallo @hugo ich bins @herbert!', hugo)
        post.save()
        self.assertEqual(post.text_template, 'hallo {u0} ich bins {u1}!')
        change_microblogging_authorship(hugo, herbert)
        post = Post.objects.get(id=post.id)  # update object from DB

        self.assertNotIn(hugo, post.mentions.all())
        self.assertIn(herbert, post.mentions.all())

        self.assertEqual(post.text_template, 'hallo {u0} ich bins {u0}!')

    def test_delete_posts_referring_to_removes_referring_posts1(self):
        hugo = create_user('hugo')
        node = create_nodes_for_path("path.1")
        create_post("foo", hugo, '/path.1')
        self.assertEqual(Post.objects.count(), 1)
        delete_posts_referring_to(node)
        self.assertEqual(Post.objects.count(), 0)

    def test_delete_node_removes_referring_posts2(self):
        hugo = create_user('hugo')
        node = create_nodes_for_path("path.1")
        create_post("foo /path.1", hugo)
        self.assertEqual(Post.objects.count(), 1)
        delete_posts_referring_to(node)
        self.assertEqual(Post.objects.count(), 0)
