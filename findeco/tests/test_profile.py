#!/usr/bin/python
# coding=utf-8
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
################################################################################
from __future__ import division, print_function, unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from ..models import UserProfile

class UserProfileTest(TestCase):
    def test_fresh_user_has_profile(self):
        u = User.objects.create_user('__test_user1', 'user@mail.de', 'password')
        self.assertTrue(UserProfile.objects.filter(user=u).count() == 1)

    def test_user_profile_is_accessible(self):
        u = User.objects.create_user('__test_user2', 'user@mail.de', 'password')
        self.assertTrue(isinstance(u.profile, UserProfile))

    def test_user_profile_has_description(self):
        u = User.objects.create_user('__test_user3', 'user@mail.de', 'password')
        self.assertEqual(u.profile.description, '')

    def test_user_profile_has_following_and_followers(self):
        u = User.objects.create_user('__test_user4', 'user@mail.de', 'password')
        self.assertEqual(u.profile.followees.count(), 0)
        self.assertEqual(u.profile.followees.count(), 0)

    def test_user_profile_is_saved_with_user(self):
        u = User.objects.create_user('__test_user5', 'user@mail.de', 'password')
        u.profile.description = 'foo'
        u.save()
        p = UserProfile.objects.filter(user=u)[0]
        self.assertEqual(p.description, 'foo')