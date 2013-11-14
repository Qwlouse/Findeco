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
from django.core.urlresolvers import reverse
from django.test import TestCase
import json
from findeco.tests.helpers import assert_is_error_response
from findeco.view_helpers import assert_node_for_path

from node_storage import get_root_node, Node, Argument
from node_storage.factory import create_user, create_slot, create_textNode
from node_storage.path_helpers import get_node_for_path


class StoreTextTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234",
                                groups=['texters', 'voters', 'bloggers'])

        create_user("Notpermitted", password="fghjfgh")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)
        self.text = create_textNode("Slotteria", "This is a textnode",
                                    authors=[self.hugo])
        self.slot.append_child(self.text)
        self.url = reverse('store_text', kwargs=dict(path="Slot.1"))

    def test_not_authenticated(self):
        response = self.client.post(self.url, dict(wikiText="= Bla =\nBlubb."))
        assert_is_error_response(response, "_NotAuthenticated")

    def test_not_permitted(self):
        self.assertTrue(
            self.client.login(username="Notpermitted", password="fghjfgh"))
        response = self.client.post(self.url, dict(wikiText="= Bla =\nBlubb."))
        assert_is_error_response(response, "_PermissionDenied")

    def test_store_missing_text(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(self.url)
        assert_is_error_response(response, "_MissingPOSTParameter")

    def test_store_missing_argument_type(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(self.url, dict(wikiText="= Hopp =\nGrumpf.",
                                                   wikiTextAlternative="= Bla =\nBlubb."))
        assert_is_error_response(response, "_MissingPOSTParameter")

    def test_store_textNode(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(self.url, dict(wikiTextAlternative="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'], "Slot.2")
        node = assert_node_for_path("Slot.2")
        self.assertEqual(node.title, "Bla")
        self.assertEqual(node.text.text, "Blubb.")

    def test_store_additionalSlot(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(self.url, dict(wikiText="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        parsed = json.loads(response.content)
        self.assertEqual(parsed['storeTextResponse']['path'], "Slot.2")
        node = assert_node_for_path("Slot.2/Bla.1")
        self.assertEqual(node.title, "Bla")
        self.assertEqual(node.text.text, "Blubb.")
        self.assertEqual(node.parents.all()[0].title, "Bla")

    def test_store_with_argument_and_alternative(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            self.url, dict(argumentType="con",
                           wikiText="= Argumenttitel =\nDas ist jetzt besser",
                           wikiTextAlternative="= Bla 2 =\nFollopp."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'], "Slot.2")
        self.assertEqual(Node.objects.filter(parents=self.slot).count(), 2)
        self.assertEqual(Node.objects.filter(parents=self.slot).all()[0].title,
                         "Slotteria")
        self.assertEqual(
            Node.objects.filter(parents=self.slot).all()[0].text.text, "This is a textnode")
        self.assertEqual(Node.objects.filter(parents=self.slot).all()[1].title,
                         "Bla 2")
        self.assertEqual(
            Node.objects.filter(parents=self.slot).all()[1].text.text,
            "Follopp.")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).count(), 1)
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].title, "Argumenttitel")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].text.text,
                         "Das ist jetzt besser")

    def test_store_with_argumente(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            self.url, dict(argumentType="con",
                           wikiText="= Argumenttitel =\nDas ist jetzt besser"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'],
            "Slot.1.con.1")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).count(), 1)
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].title, "Argumenttitel")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].text.text,
                         "Das ist jetzt besser")

    def test_add_derivate_preserves_substructure(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        text_string = "= Bla =\nBlubb.\n== Level 2 ==\nSome text."
        response = self.client.post(self.url, dict(wikiTextAlternative=text_string))
        self.assertEqual(response.status_code, 200)
        text_string2 = text_string + "\n== Another Level 2 ==\nSome other text."
        response = self.client.post(
            "/.json_storeText/Slot.2", dict(argumentType="con",
                           wikiText="= Argumenttitle =\nThis is better now.",
                           wikiTextAlternative=text_string2))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['storeTextResponse']['path'], "Slot.3")
        new_node = get_node_for_path('Slot.3')
        self.assertEqual(new_node.text.text, "Blubb.")
        self.assertEqual(new_node.children.all()[0].children.all()[0].text.text,
                         "Some text.")
        self.assertEqual(new_node.children.all()[1].children.all()[0].text.text,
                         "Some other text.")
        old_node = get_node_for_path('Slot.2')
        self.assertEqual(new_node.children.all()[0].children.all()[0],
                         old_node.children.all()[0].children.all()[0])