from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import *  # available since 2.4.0
from selenium.webdriver.support.wait import WebDriverWait
# from __future__ import division, print_function, unicode_literals
from django.test import LiveServerTestCase
import time



class TestFePageLogin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)
    def tearDown(self):
        self.driver.quit()

    def test_check_page_Contents(self):
        self.driver.get(self.live_server_url + '/login')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Mit dem Login', body.text, "Partial not loaded")
 # WebDriverWait(self.selenium, timeout).until(
        # lambda driver: driver.find_element_by_tag_name('body'))

    def test_check_invalid_login(self):
        self.driver.get(self.live_server_url + '/login')
        self.driver.implicitly_wait(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Mit dem Login', body.text, "Partial not loaded")
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("password")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("benutzer")
        self.driver.find_element_by_css_selector("input.btn.btn-primary").click()
        tmp = self.driver.find_element_by_tag_name('span').text
        self.assertIn('Der Benutzer ist dem System nicht bekannt', tmp , "No Message on wrong Login")

    def test_check_login(self):
        self.driver.get(self.live_server_url + '/login')
        self.driver.implicitly_wait(1)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Mit dem Login', body.text, "Partial not loaded")
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("1234")
        self.driver.find_element_by_xpath("//input[@ng-model='username']").send_keys("admin")
        self.driver.find_element_by_css_selector("input.btn.btn-primary").click()
        time.sleep(2)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('admin', body.text, "Login without success")



