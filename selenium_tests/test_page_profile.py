#!/usr/bin/python
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
import time


@attr('selenium')
class TestFePageProfile(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()
    def login(self):
        self.driver.get(self.live_server_url + '/login')
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("1234")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin")
        self.driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('admin', body.text, "Login without success")

    def test_change_user_description(self):
        self.driver.get(self.live_server_url + '/')
        self.login()
        self.driver.find_element_by_link_text("admin").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//textarea[@ng-model='user.description']").send_keys("Dies ist die Userbeschreibung")
        time.sleep(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Dies ist die Userbeschreibung', body.text, "Preview does not work")
        self.driver.find_element_by_css_selector("input[type='submit']").click()
        self.driver.find_elements_by_css_selector(".alert-success")
        self.driver.find_element_by_css_selector("button.close").click()
    
    def test_change_user_email(self):
        self.login()
        self.driver.get(self.live_server_url + '/profile/mail')
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("")
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("footrash-mail.com")
        self.driver.find_element_by_xpath("(//input[@value='Speichern'])[1]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_css_selector("button.close").click()
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("foo@trash-mail.com")

    def test_change_user_name(self):
        self.login()
        self.driver.get(self.live_server_url + '/profile')
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").clear()
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("")
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("admin")
        self.driver.find_element_by_xpath("(//input[@value='Speichern'])[1]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_css_selector("button.close").click()
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("")
        self.driver.find_element_by_xpath("(//input[@type='text'])[1]").send_keys("admin2")
        self.driver.find_element_by_xpath("(//input[@value='Speichern'])[1]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert-success")))
        
    def test_change_password(self):
        self.login()
        self.driver.get(self.live_server_url + '/profile/password')
        self.driver.find_element_by_xpath("(//input[@type='password'])[1]").clear()
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").clear()
        self.driver.find_element_by_xpath("(//input[@type='password'])[1]").send_keys("foobar")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("foo")
        self.driver.find_element_by_xpath("(//input[@value='Speichern'])[1]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_css_selector("button.close").click()
        self.driver.find_element_by_xpath("(//input[@type='password'])[1]").clear()
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").clear()
        self.driver.find_element_by_xpath("(//input[@type='password'])[1]").send_keys("foo")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("foo")
        self.driver.find_element_by_xpath("(//input[@value='Speichern'])[1]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert-success")))
        self.driver.find_element_by_css_selector("img[alt=\"Logout\"]").click()
        self.driver.get(self.live_server_url + '/login')
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("foo")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin")
        self.driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('admin', body.text, "Login without success")
        
  #  def test_delete_user(self):
     #   self.login()
     #  self.driver.get(self.live_server_url + '/profile/delete')
    #    self.driver.find_element_by_xpath("(//input[@value='Account löschen'])[1]").click()
   #    self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
    #   
