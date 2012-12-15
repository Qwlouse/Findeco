#!/usr/bin/python
# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib.auth.models import User
import unittest

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
