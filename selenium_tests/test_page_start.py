from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
# from __future__ import division, print_function, unicode_literals
from django.test import LiveServerTestCase
import time


class TestFePageStart(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(1)
    def tearDown(self):
        self.driver.quit()
    def test_check_page_Contents(self):
        
        self.driver.get(self.live_server_url)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('DisQussion', body.text, "defaut Json file for external content not loaded")
        self.assertNotIn("{", body.text , "Angular not loaded")
        self.assertIs(self.driver.find_element_by_css_selector(".deactivateSpinner").is_displayed(), False, "A Spinner stays displayed")

