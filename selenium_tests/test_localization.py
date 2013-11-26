#!/usr/bin/python
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2013 Michael Zaspel <michaelzaspel@web.de.de>
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
from django.test import LiveServerTestCase
from nose.plugins.attrib import attr
from test_helper import helper_login_admin
from selenium import webdriver
import time
@attr('selenium')
class TestFeLocalization(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def test_profile_localizations(self):
        """
        Checks all listed Pages for missing localization strings.
        @param self:
        """
        helper_login_admin(self)
        time.sleep(1)
        self.driver.get(self.live_server_url + '/profile')
        self.assertNotIn('_', self.driver.find_element_by_tag_name('body').text, "Localization on profile not done")
        self.driver.get(self.live_server_url + '/profile/password')
        self.assertNotIn('_', self.driver.find_element_by_tag_name('body').text, "Localization on profile password not done")