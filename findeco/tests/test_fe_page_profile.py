from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import *  # available since 2.4.0

# from __future__ import division, print_function, unicode_literals
from django.test import LiveServerTestCase
import time



class TestFePageProfile(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)
    def tearDown(self):
        self.driver.quit()

    def test_change_user_description(self):
        self.driver.get(self.live_server_url + '/')
        self.driver.find_element_by_link_text("admin").click()
        self.driver.find_element_by_xpath("//textarea[@ng-model='user.description']").send_keys("Dies ist die Userbeschreibung")
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Dies ist die Userbeschreibung', body.text, "Preview does not work")
