#!/usr/bin/env python3
# coding=utf-8
# region License
# Findeco is dually licensed under GPLv3 or later and MPLv2.
#
###############################################################################
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
###############################################################################
#
###############################################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# endregion ###################################################################

from django.core import mail
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time


class TestFePageRegistration(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def test_check_click_path_to_page(self):
        self.driver.get(self.live_server_url + '/')
        self.driver.find_element_by_link_text("Anmelden").click()
        self.driver.find_element_by_link_text("Noch kein Account? Hier registrieren").click()

    def test_check_page_Contents(self):
        self.driver.get(self.live_server_url + '/register')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Die Accountregistrierung steht', body.text, "Partial not loaded")

    def test_check_form_validation(self):
        # Without content
        self.driver.get(self.live_server_url + '/register')
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('alle Felder ausgef', tmp, "Message fill all fields is missing - when submitting without filled forms")
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Du musst die Nutzungsbedingungen', tmp, "Message check tos is missing - when submitting without filled forms")
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Du musst die Datenschutzbestimmung', tmp, "Message check DPR is missing - when submitting without filled forms")
        self.assertNotRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*_[\s\S]*$")

        # non matching password
        self.driver.get(self.live_server_url + '/register')
        self.assertEqual(0, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").send_keys(" ")
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").send_keys(" ")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin2")
        self.driver.find_element_by_xpath("(//input[@type='password'])").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("password1")
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("a@trash-mail.com")
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Die eingegebenen Pass', tmp, "Message - Non matching Passwords missing")
        self.assertNotRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*_[\s\S]*$")

        # Invalid mailaddress
        self.driver.get(self.live_server_url + '/register')
        self.assertEqual(0, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").send_keys(" ")
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").send_keys(" ")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin2")
        self.driver.find_element_by_xpath("(//input[@type='password'])").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("a@trash-macom")
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Emailadresse ist ung', tmp , "Message - Invalid mail missing")
        self.assertNotRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*_[\s\S]*$")

    def test_username_already_taken(self):
        self.driver.get(self.live_server_url + '/register')
        self.assertEqual(0, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").send_keys(" ")
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").send_keys(" ")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin")
        self.driver.find_element_by_xpath("(//input[@type='password'])").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("a@trash-mail.com")
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert")))
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Benutzername ist nicht verf', tmp , "Message missing - Username already taken")
        self.assertNotRegexpMatches(self.driver.find_element_by_css_selector("BODY").text, r"^[\s\S]*_[\s\S]*$")

    def test_full_registration_process(self):
        self.driver.get(self.live_server_url + '/register')
        self.assertEqual(0, len(self.driver.find_elements_by_css_selector(".alert")))
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("testuser")
        self.driver.find_element_by_xpath("(//input[@type='password'])").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='password'])[2]").send_keys("password")
        self.driver.find_element_by_xpath("(//input[@type='text'])[2]").send_keys("fin@trash-mail.com")
        self.driver.find_element_by_xpath("//input[@type='checkbox']").click()
        self.driver.find_element_by_xpath("(//input[@type='checkbox'])[2]").click()
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        time.sleep(3)
        self.assertEqual(1, len(self.driver.find_elements_by_css_selector(".alert-success")))
        self.assertEquals(len(mail.outbox), 1)
        activation_url = mail.outbox[0].body.split(':8000')[1].split()[0]
        self.driver.get(self.live_server_url + activation_url)
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Dein Account wurde aktiviert.', tmp, "Activation Failed")
        self.driver.get(self.live_server_url + mail.outbox[0].body.split(":8000")[1])
        tmp = self.driver.find_element_by_tag_name('body').text
        time.sleep(10)
        self.assertIn('ltiger Aktivierungscode', tmp, "Activation Key not invalidated")
        time.sleep(10)
        self.driver.get(self.live_server_url + '/login')
        self.driver.implicitly_wait(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Mit dem Login', body.text, "Partial not loaded")
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("password")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("testuser")
        self.driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(2)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('testuser', body.text, "Login without success")