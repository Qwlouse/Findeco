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
import json
from django.test import TestCase
from findeco.tests.test_views import userInfoValidator
from node_storage.factory import create_user
from ..view_helpers import create_user_info

class ViewHelpersTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', "he's a jolly good fellow")
        self.hugo = create_user('hugo', "nodescription")
        self.hein = create_user('hein', "password1")
        self.users = [self.hans, self.hugo, self.hein]

        self.hugo.profile.followees.add(self.hans.profile)
        self.hein.profile.followees.add(self.hans.profile)

    def test_create_user_info_validates(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertTrue(userInfoValidator.validate(user_info))

    def test_create_user_info_contains_correct_username(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertEqual(user_info['displayName'], user.username)

    def test_create_user_info_contains_correct_description(self):
        for user in self.users:
            user_info = create_user_info(user)
            self.assertEqual(user_info['description'], user.profile.description)

    def test_create_user_info_contains_correct_followers(self):
        user_info = create_user_info(self.hans)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 2)
        self.assertIn({'displayName':'hugo'}, followers)
        self.assertIn({'displayName':'hein'}, followers)

        user_info = create_user_info(self.hugo)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 0)

        user_info = create_user_info(self.hein)
        self.assertIn('followers', user_info)
        followers = user_info['followers']
        self.assertEqual(len(followers), 0)


    def test_create_user_info_contains_correct_followees(self):
        user_info = create_user_info(self.hans)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 0)

        user_info = create_user_info(self.hugo)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 1)
        self.assertIn({'displayName':'hans'}, followees)

        user_info = create_user_info(self.hein)
        self.assertIn('followees', user_info)
        followees = user_info['followees']
        self.assertEqual(len(followees), 1)
        self.assertIn({'displayName':'hans'}, followees)


