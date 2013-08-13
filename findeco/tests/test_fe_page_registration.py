from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import *  # available since 2.4.0

# from __future__ import division, print_function, unicode_literals
from django.test import LiveServerTestCase
import time



class TestFePageRegistration(LiveServerTestCase):
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

    def test_check_form_valifation(self):
        # Without content
        self.driver.get(self.live_server_url + '/register')
        self.driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('alle Felder ausgef', tmp , "Message fill all fields is missing - when submitting without filled forms")
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Du musst die Nutzungsbedingungen', tmp , "Message check tos is missing - when submitting without filled forms")
        tmp = self.driver.find_element_by_tag_name('body').text
        self.assertIn('Du musst die Datenschutzbestimmung', tmp , "Message check DPR is missing - when submitting without filled forms")
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
        self.assertIn('Die eingegebenen Pass', tmp , "Message - Non matching Passwords missing")
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
        time.sleep(2)
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
       # self.assertEqual(0, len(self.driver.find_elements_by_css_selector(".alert")))
        '''@todo: Registration is not completed thus mail problems in testing env'''
        '''@todo: Ensure Activation code is invalidated'''
       # time.sleep(20)
        # self.driver.get("http://www.trash-mail.com")
       # self.driver.find_element_by_name("mail").click()
        # self.driver.find_element_by_name("mail").clear()
        # self.driver.find_element_by_name("mail").send_keys("fin")
        # self.driver.find_element_by_name("submit").click()
        # self.assertTrue(self.is_element_present(By.LINK_TEXT, "Your Findeco registration"))
        # self.driver.find_element_by_link_text("Your Findeco registration").click()
        # self.driver.find_element_by_css_selector(".mail_content a").click()




