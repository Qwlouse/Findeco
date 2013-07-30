#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Johannes Merkert <jonny@pinae.net>
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

from django.test import TestCase
from findeco.tests.helpers import assert_is_error_response
from node_storage.factory import create_slot, create_textNode
from node_storage.factory import create_user, create_vote
from ..models import create_post
from django.core.urlresolvers import reverse
import node_storage as backend
from ..models import Post
import json

ROOT_SYMBOL = "/"


class StoreMicrobloggingTests(TestCase):
    def setUp(self):
        self.user_max = create_user("max", password="1234")

        root = backend.get_root_node()
        slot1 = create_slot("Bla")
        root.append_child(slot1)

        self.text_node1 = create_textNode("Whatever", "Testtext",
                                          [self.user_max])
        slot1.append_child(self.text_node1)

        slot2 = create_slot("Blubb")
        root.append_child(slot2)

        text_node2 = create_textNode("Whatever2", "Testtext Nummer 2",
                                     [self.user_max])
        slot2.append_child(text_node2)

    def test_store_microblog_post(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.post(
            reverse('store_microblog_post', kwargs=dict(path="Bla.1")),
            dict(microblogText="Bla bla bla. I had to say it."),
            HTTP_HOST="findecotest:4321")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(
            Post.objects.filter(text="Bla bla bla. I had to say it.").all()), 1)

    def test_store_microblog_post_with_reference(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.post(
            reverse('store_microblog_post', kwargs=dict(path="Bla.1")),
            dict(microblogText="Bla bla bla. I have to reference /bla.1."),
            HTTP_HOST="findecotest:4321")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(
            Post.objects.filter(text="Bla bla bla. I have to reference /bla.1.").all()), 1)

    def test_store_microblog_post_with_long_url_reference(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.post(
            reverse('store_microblog_post', kwargs=dict(path="Bla.1")),
            dict(microblogText="Bla bla bla. I have to reference http://findecotest:4321/bla.1."),
            HTTP_HOST="findecotest:4321")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(
            Post.objects.filter(text="Bla bla bla. I have to reference /bla.1.").all()), 1)

    def test_store_microblog_post_not_authenticated(self):
        response = self.client.post(
            reverse('store_microblog_post', kwargs=dict(path="Bla.1")),
            dict(microblogText="Bla bla bla. I had to say it."))
        assert_is_error_response(response, '_NotAuthenticated')


class MicrobloggingTests(TestCase):
    def setUp(self):
        self.user_max = create_user("max", password="1234")
        self.user_maria = create_user("Maria")

        root = backend.get_root_node()
        slot1 = create_slot("Bla")
        root.append_child(slot1)

        self.text_node1 = create_textNode("Whatever", "Testtext",
                                          [self.user_max])
        slot1.append_child(self.text_node1)

        slot2 = create_slot("Blubb")
        root.append_child(slot2)

        text_node2 = create_textNode("Whatever2", "Testtext Nummer 2",
                                     [self.user_max])
        slot2.append_child(text_node2)

        self.posts = []
        for i in range(25):
            self.posts.append(
                create_post("Ich finde /Bla.1 gut.", self.user_max))
        self.posts.append(
            create_post("Ich finde /Blubb.1 schlecht.", self.user_max))
        create_vote(self.user_max, [self.text_node1])

    def test_post_creation(self):
        all_posts = Post.objects.all()
        self.assertSequenceEqual(all_posts, self.posts)
        self.assertEqual(
            all_posts[0].text,
            'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
        self.assertEqual(all_posts[0].author, self.user_max)
        self.assertEqual(all_posts[0].id, 1)
        self.assertSequenceEqual(all_posts[0].node_references.all(),
                                 [self.text_node1])

    def test_load_microblogging_illegal_path(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Slot_4.1/SubSlot_1.1",
                                select_id=0,
                                microblogging_load_type="newer")))
        assert_is_error_response(response, '_UnknownNode')

    def test_load_microblogging_0_newer(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Bla.1",
                    select_id=0,
                    microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue(
                'microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue(
                'microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogID'], 19 - i + 1)
            self.assertTrue(
                'authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue(
                'microblogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)

    def test_load_microblogging_no_select_id(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Bla.1",
                                select_id=None,
                                microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)
        for i in range(20):
            self.assertTrue('microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue('microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microblogID'], 25 - i)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue('microblogTime' in data['loadMicrobloggingResponse'][i])

    def test_load_microblogging_3_newer(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Bla.1",
                                select_id=3,
                                microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue(
                'microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue(
                'microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogID'], 19 - i + 4)
            self.assertTrue(
                'authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue(
                'microblogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)

    def test_load_microblogging_6_newer(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Bla.1",
                    select_id=6,
                    microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(19):
            self.assertTrue(
                'microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue(
                'microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogID'], 18 - i + 7)
            self.assertTrue(
                'authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue(
                'microblogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']), 19)

    def test_load_microblogging_23_older(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Bla.1",
                    select_id=23,
                    microblogging_load_type="older")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)
        for i in range(20):
            self.assertTrue('microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microblogText'],
                             'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue('microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microblogID'], 19 - i + 3)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue('microblogTime' in data['loadMicrobloggingResponse'][i])

    def test_load_microblogging_only_one_post(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_microblogging',
                    kwargs=dict(path="Blubb.1",
                    select_id=0,
                    microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertEqual(len(data['loadMicrobloggingResponse']), 1)
        self.assertTrue('microblogText' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microblogText'],
                         'Ich finde <a href="' + ROOT_SYMBOL +
                         'Blubb.1">Whatever2</a> schlecht.')
        self.assertTrue('microblogID' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microblogID'],
                         26)
        self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(
            len(data['loadMicrobloggingResponse'][0]['authorGroup']), 1)
        self.assertTrue('microblogTime' in data['loadMicrobloggingResponse'][0])

    def test_load_timeline_with_select_id(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_timeline',
                    kwargs=dict(name="max", select_id=0,
                                microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        for i in range(20):
            self.assertTrue(
                'microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue(
                'microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogID'], 19 - i + 1)
            self.assertTrue(
                'authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue(
                'microblogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)

    def test_load_timeline_without_select_id(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_timeline',
                    kwargs=dict(name="max",
                                select_id=None,
                                microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertTrue('microblogText' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microblogText'],
                         'Ich finde <a href="' + ROOT_SYMBOL +
                         'Blubb.1">Whatever2</a> schlecht.')
        self.assertTrue('microblogID' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(data['loadMicrobloggingResponse'][0]['microblogID'],
                         26)
        self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][0])
        self.assertEqual(
            len(data['loadMicrobloggingResponse'][0]['authorGroup']), 1)
        self.assertTrue('microblogTime' in data['loadMicrobloggingResponse'][0])
        for i in range(1, 20):
            self.assertTrue(
                'microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue(
                'microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogID'], 26 - i)
            self.assertTrue(
                'authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue(
                'microblogTime' in data['loadMicrobloggingResponse'][i])
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)

    def test_load_collection_without_select_id(self):
        self.assertTrue(self.client.login(username="max", password="1234"))

        response = self.client.get(
            reverse('load_collection', kwargs=dict(select_id=None, microblogging_load_type="newer")))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('loadMicrobloggingResponse' in data)
        self.assertEqual(len(data['loadMicrobloggingResponse']), 20)
        for i in range(0, 20):
            self.assertTrue('microblogText' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(
                data['loadMicrobloggingResponse'][i]['microblogText'],
                'Ich finde <a href="' + ROOT_SYMBOL + 'Bla.1">Whatever</a> gut.')
            self.assertTrue('microblogID' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(data['loadMicrobloggingResponse'][i]['microblogID'], 25 - i)
            self.assertTrue('authorGroup' in data['loadMicrobloggingResponse'][i])
            self.assertEqual(len(data['loadMicrobloggingResponse'][i]['authorGroup']), 1)
            self.assertTrue('microblogTime' in data['loadMicrobloggingResponse'][i])