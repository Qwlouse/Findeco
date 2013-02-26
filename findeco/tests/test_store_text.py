#!/usr/bin/python
# coding=utf-8
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>,
# Johannes Merkert <jonny@pinae.net>
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
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.test import TestCase
import json

from node_storage import get_root_node, Node, Argument
from node_storage.factory import create_user, create_slot


class StoreTextTest(TestCase):
    def setUp(self):
        self.root = get_root_node()
        self.hugo = create_user("Hugo", password="1234",
                                groups=['texters', 'voters', 'bloggers'])

        create_user("Notpermitted", password="fghjfgh")
        self.slot = create_slot("Slot")
        self.root.append_child(self.slot)

    def test_not_authenticated(self):
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['errorResponse']['errorTitle'],
            ugettext("NotAuthenticated"))

    def test_not_permitted(self):
        self.assertTrue(
            self.client.login(username="Notpermitted", password="fghjfgh"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['errorResponse']['errorTitle'],
            ugettext("PermissionDenied"))

    def test_store_textNode(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'], "Slot.1")
        self.assertEqual(Node.objects.filter(parents=self.slot).count(), 1)
        self.assertEqual(Node.objects.filter(parents=self.slot).all()[0].title,
                         "Bla")
        self.assertEqual(
            Node.objects.filter(parents=self.slot).all()[0].text.text, "Blubb.")

    def test_store_missing_text(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['errorResponse']['errorTitle'],
            ugettext("MissingPostParameter"))

    def test_store_missing_argument_type(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Hopp =\nGrumpf.",
                 wikiTextAlternative="= Bla =\nBlubb."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['errorResponse']['errorTitle'],
            ugettext("MissingPostParameter"))

    def test_store_with_argument_and_alternative(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Bla =\nBlubb."))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(argumentType="con",
                 wikiText="= Argumenttitel =\nDas ist jetzt besser",
                 wikiTextAlternative="= Bla 2 =\nFollopp."))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'], "Slot.2")
        self.assertEqual(Node.objects.filter(parents=self.slot).count(), 2)
        self.assertEqual(Node.objects.filter(parents=self.slot).all()[0].title,
                         "Bla")
        self.assertEqual(
            Node.objects.filter(parents=self.slot).all()[0].text.text, "Blubb.")
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
            "= Argumenttitel =\nDas ist jetzt besser")

    def test_store_with_argumente(self):
        self.assertTrue(self.client.login(username="Hugo", password="1234"))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(wikiText="= Bla =\nBlubb."))
        response = self.client.post(
            reverse('store_text', kwargs=dict(path="Slot.1")),
            dict(argumentType="con",
                 wikiText="= Argumenttitel =\nDas ist jetzt besser"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)['storeTextResponse']['path'],
            "Slot.1.con.1")
        self.assertEqual(Node.objects.filter(parents=self.slot).count(), 1)
        self.assertEqual(Node.objects.filter(parents=self.slot).all()[0].title,
                         "Bla")
        self.assertEqual(
            Node.objects.filter(parents=self.slot).all()[0].text.text, "Blubb.")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).count(), 1)
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].title, "Argumenttitel")
        self.assertEqual(Argument.objects.filter(concerns=Node.objects.filter(
            parents=self.slot).all()[0]).all()[0].text.text,
            "= Argumenttitel =\nDas ist jetzt besser")