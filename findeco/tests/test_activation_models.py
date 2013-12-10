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
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Activation, EmailActivation, PasswordRecovery
from node_storage.factory import create_user


class ActivationTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans')
        self.hans.is_active = False

    def test_activation_creation(self):
        act = Activation.create(self.hans)
        self.assertEqual(act.user, self.hans)
        self.assertTrue(act.is_valid())
        self.assertTrue(len(act.key) > 60)

    def test_activation_resolve(self):
        act = Activation.create(self.hans)
        self.assertTrue(act.resolve())
        hans = User.objects.get(id=self.hans.id)
        self.assertTrue(hans.is_active)


class EmailActivationTest(TestCase):
    def setUp(self):
        self.hans = create_user('hans', mail="abc@de.com")
        self.hans.is_active = True

    def test_email_activation_creation(self):
        act = EmailActivation.create(self.hans, 'zyx@wvu.moc')
        self.assertEqual(act.user, self.hans)
        self.assertEqual(act.new_email, 'zyx@wvu.moc')
        self.assertTrue(len(act.key) > 60)

    def test_email_activation_resolve(self):
        act = EmailActivation.create(self.hans, 'zyx@wvu.moc')
        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.email, 'abc@de.com')
        self.assertTrue(act.resolve())
        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.email, 'zyx@wvu.moc')

    def test_email_activations_overwrite_each_other(self):
        act1 = EmailActivation.create(self.hans, 'mail1@abc.de')
        act2 = EmailActivation.create(self.hans, 'mail2@abc.de')
        self.assertEqual(EmailActivation.objects.filter(user=self.hans).count(),
                         1)
        act = EmailActivation.objects.get(user=self.hans)
        self.assertTrue(act.resolve())
        hans = User.objects.get(id=self.hans.id)
        self.assertEqual(hans.email, 'mail2@abc.de')


class PasswordRecoveryTest(TestCase):
    def test_recovery_creation(self):
        hans = create_user('hans')
        act = PasswordRecovery.create(hans)
        self.assertEqual(act.user, hans)
        self.assertTrue(act.is_valid())
        self.assertTrue(len(act.key) > 60)

    def test_recovery_resolve(self):
        hans = create_user('hans', password="forgotten")
        act = PasswordRecovery.create(hans)
        pw = act.resolve()
        self.assertTrue(pw)
        self.assertIsNone(authenticate(username='hans', password='forgotten'))
        self.assertEqual(authenticate(username='hans', password=pw), hans)
