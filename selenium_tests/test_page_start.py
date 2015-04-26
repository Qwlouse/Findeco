#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
################################################################################
# Copyright (c) 2013 Maik Nauheim <findeco@maik-nauheim.de>
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
from selenium import webdriver


@attr('selenium')
class TestFePageStart(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def test_check_page_Contents(self):
        self.driver.get(self.live_server_url + '/start')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('DisQussion', body.text, "defaut Json file for external content not loaded")
        self.assertNotIn("{", body.text , "Angular not loaded")
        self.assertIs(self.driver.find_element_by_css_selector(".deactivateSpinner").is_displayed(), False, "A Spinner stays displayed")

