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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
import json
from findeco.api_validation import storeSettingsResponseValidator
from findeco.tests.helpers import assert_is_error_response

from node_storage.factory import create_user, create_slot, create_textNode

from ..api_validation import loadUserInfoResponseValidator
from ..api_validation import loadUserSettingsResponseValidator
from ..view_helpers import create_user_info, create_user_settings


class LoadUserInfoTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.herbert = create_user('herbert')
        self.hein = create_user('hein')
        self.users = [self.hans, self.herbert, self.hein]

    def test_with_valid_username_returns_correct_user_info(self):
        for u in self.users:
            response = self.client.get(
                reverse('load_user_info', kwargs=dict(name=u.username)))
            parsed = json.loads(response.content)
            self.assertTrue(loadUserInfoResponseValidator.validate(parsed))
            user_info = create_user_info(u)
            self.assertEqual(parsed['loadUserInfoResponse']['userInfo'],
                             user_info)

    def test_with_invalid_username_returns_error_response(self):
        for n in ['hannes', 'harbart', 'nieh']:
            response = self.client.get(
                reverse('load_user_info', kwargs=dict(name=n)))
            assert_is_error_response(response, "_UnknownUser")


class LoadUserSettingsTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', password="1234")
        self.herbert = create_user('herbert', password="1234")
        self.hans.profile.blocked.add(self.herbert.profile)
        self.users = [self.hans, self.herbert]

    def test_response_validates(self):
        for u in self.users:
            self.assertTrue(
                self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertTrue(loadUserSettingsResponseValidator.validate(parsed))

    def test_returns_correct_user_info_for_logged_in_user(self):
        for u in self.users:
            self.assertTrue(
                self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertEqual(parsed['loadUserSettingsResponse']['userInfo'],
                             create_user_info(u))

    def test_returns_correct_user_settings_for_logged_in_user(self):
        for u in self.users:
            self.assertTrue(
                self.client.login(username=u.username, password='1234'))
            response = self.client.get(reverse('load_user_settings'))
            parsed = json.loads(response.content)
            self.assertEqual(parsed['loadUserSettingsResponse']['userSettings'],
                             create_user_settings(u))

    def test_not_logged_in_returns_error_response(self):
        response = self.client.get(reverse('load_user_settings'))
        assert_is_error_response(response, "_NotAuthenticated")


class StoreSettingsTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', description='noneSoFar',
                                password="1234")
        self.post = lambda a, b: self.client.post(
            a, json.dumps(b), content_type='application/json')

    def test_response_validates(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.post(reverse('store_settings'),
                                    dict(description="", displayName='hans', email='a@bc.de'))
        parsed = json.loads(response.content)
        self.assertTrue(storeSettingsResponseValidator.validate(parsed))

    def test_missing_description_parameter_returns_error(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.post(reverse('store_settings'),
                             dict(displayName='hans'))
        assert_is_error_response(response, "_MissingPOSTParameter")

    def test_missing_displayname_parameter_returns_error(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.post(reverse('store_settings'),
                             dict(description=''))
        assert_is_error_response(response, "_MissingPOSTParameter")

    def test_unavailable_displayname_returns_error(self):
        self.hugo = create_user('hugo', description='notHulk', password="1234")
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.post(reverse('store_settings'),
                             dict(displayName='hugo', description=''))
        assert_is_error_response(response, "_UsernameNotAvailable")

    def test_change_description_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        _ = self.post(reverse('store_settings'),
                      dict(description="foo", displayName='hans', email='a@bc.de'))
        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.profile.description, "foo")

    def test_change_username_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        _ = self.post(reverse('store_settings'),
                      dict(description="foo", displayName='hans2', email='a@bc.de'))
        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.username, "hans2")

    def test_change_wants_mail_notification_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        self.assertEqual(self.hans.profile.wants_mail_notification, False)

        _ = self.post(reverse('store_settings'),
                      dict(description="foo", displayName='hans',
                           email='a@bc.de', wantsMailNotification=True))

        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.profile.wants_mail_notification, True)

    def test_change_wants_no_mail_notification_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        self.assertEqual(self.hans.profile.wants_mail_notification, False)

        _ = self.post(reverse('store_settings'),
                      dict(description="foo", displayName='hans',
                           email='a@bc.de', wantsMailNotification=False))

        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.profile.wants_mail_notification, False)


class ChangePasswordTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', description='noneSoFar',
                                password="1234")

    def test_change_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.client.post(
            reverse('change_password'),
            json.dumps(dict(password="foo")),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.assertTrue(self.client.login(username="hans", password='foo'))


class DeleteUserTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', description='noneSoFar',
                                password="1234")
        self.karl = create_user('karl', description='none',
                                password="blubb")
        self.anon = User.objects.filter(username='anonymous').all()[0]
        self.slot = create_slot("test")
        self.text1 = create_textNode("Hans Text", "Ich werde anonymisiert", [self.hans])
        self.text2 = create_textNode("Karls Text", "Ich werde nicht anonymisiert", [self.karl])
        self.text3 = create_textNode("Gemeinsamer Text", "Anonymous wird dabei geholfen haben diesen Text zu erstellen",
                                     [self.hans, self.karl])
        self.text4 = create_textNode("Gemeinsamer Text mit anonymous",
                                     "Anonymous wird dabei geholfen haben diesen Text zu erstellen",
                                     [self.hans, self.karl, self.anon])

    def test_delete_works(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.client.post(reverse('delete_user'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.login(username="hans", password='1234'))

    def test_delete_sets_author_to_anonymous(self):
        self.assertTrue(self.client.login(username="hans", password='1234'))
        response = self.client.post(reverse('delete_user'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.client.login(username="hans", password='1234'))
        self.assertNotIn(self.hans, self.text1.text.authors.all())
        self.assertNotIn(self.hans, self.text2.text.authors.all())
        self.assertNotIn(self.hans, self.text3.text.authors.all())
        self.assertNotIn(self.hans, self.text4.text.authors.all())
        self.assertIn(self.anon, self.text1.text.authors.all())
        self.assertIn(self.anon, self.text3.text.authors.all())
        self.assertIn(self.anon, self.text4.text.authors.all())
        self.assertIn(self.karl, self.text3.text.authors.all())
        self.assertIn(self.karl, self.text4.text.authors.all())
        self.assertEqual(len(self.text4.text.authors.all()),2)