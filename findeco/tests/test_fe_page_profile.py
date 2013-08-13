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
        '''@todo: Check Activation Mail'''
        '''@todo: Validate invalidation of auth code'''
    
    