#!/usr/bin/python
# coding=utf-8
# CoDebAr is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2012 Klaus Greff <klaus.greff@gmx.net>
# This file is part of CoDebAr.
#
# CoDebAr is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# CoDebAr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# CoDebAr. If not, see <http://www.gnu.org/licenses/>.
################################################################################
#
################################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
################################################################################
from __future__ import division, print_function, unicode_literals

from django.contrib.auth.models import User
import unittest

from codebar.paths import pathMatcher
from .models import UserProfile

class UserProfileTest(unittest.TestCase):
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
        self.assertEqual(u.profile.following.count(), 0)
        self.assertEqual(u.profile.followers.count(), 0)

    def test_user_profile_is_saved_with_user(self):
        u = User.objects.create_user('__test_user5', 'user@mail.de', 'password')
        u.profile.description = 'foo'
        u.save()
        p = UserProfile.objects.filter(user=u)[0]
        self.assertEqual(p.description, 'foo')

########################### Test path RE #######################################
class PathRegExTest(unittest.TestCase):
    def test_matches_valid_paths(self):
        valid_paths = [
            "/",
            "/Bildung",
            "/Bildung/",
            "/Bildung.2",
            "/Bildung.8/",
            "/Bildung.6/Einleitung",
            "/Bildung.7/Einleitung.4",
            "/Bildung.1/Einleitung.3/Praeamble.7",
            "/Bildung.1/Einleitung.3/Praeamble.7/first.1/second.2/third.3/fourth",
            "/JustTwentyCharacters",
            "/JustTwentyCharacters.20",
            "/JustTwentyCharacters.20/JustTwentyCharacters.20/JustTwentyCharacters.20/",
            "/Hy-phens.3/Under_scores.4/Numb3rs.1",
            "/A1234.4321/B123",
            "/longID.1234567890/is_ok",
            "/path.4/with.2/argument.2.pro",
            "/path.4/with.2/argument.2.con",
            "/path.4/with.2/argument.2.neut",
            "/path.4/with.2/argument.2.pro.2",
            "/path.4/with.2/argument.2.neut.4",
            "/path.4/with.2/argument.2.con.7"
        ]
        for vp in valid_paths:
            self.assertEqual(pathMatcher.match(vp).group(), vp)

    def test_does_not_match_invalid_paths(self):
        invalid_paths = [
            "noStartingSlash",
            "noStartingSlash.12/but_rest_ok.1",
            "/two.dots.12/foo",
            "/missing.3.slash.3"
            "/worng.1D/foo",
            "/1stCharIsNumber.2/foo.12",
            "/MoreThanTwentyCharacters.4/foo.12",
            "/foo.2/MoreThanTwentyCharacters",
            "/umläut.4/foo",
            "/unallow$d.1/foo.2",
            "/unallow#d.2/foo.2",
            "/unallow|d.3/foo.2",
            "/unallow:d.4/foo.2",
            "/unallow?d.5/foo.2",
            "/path.4/with.2/argument.2.pro/inbetween",
            "/path.4/with.2/argument.2.neut/inbetween",
            "/path.4/with.2/argument.2.con/inbetween",
            "/path.4/with.2/argument.2.pro.2/inbetween",
            "/path.4/with.2/argument.2.neut.7/inbetween",
            "/path.4/with.2/argument.2.con.6/inbetween",
            ]
        for ip in invalid_paths:
            self.assertNotEqual(pathMatcher.match(ip).group(), ip)
