from django.test import Client #, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from django.utils import timezone
import time
#import unittest

class NewCVTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        self.user = User.objects.create_user(
            username='Kassandra',
            password='malaka',
            email='test1@test1.com',
        )

    def tearDown(self):
        self.browser.quit()

    def test_user_can_see_blog_posts_and_signup(self):
        self.browser.get(self.live_server_url)

    # User is on the home page, clicks the CV builder link on the navbar
        self.browser.find_element_by_id("cv_builder").click()
    # User goes to CV builder, login is required so logs in
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/accounts/login/?next=/cv/")
        self.browser.find_element_by_id('login_username').send_keys("Kassandra")
        self.browser.find_element_by_id('login_password').send_keys("malaka")
        self.browser.find_element_by_id('login_submit').click()
    # After login he is redirected to CV builder and finds two buttons - edit existing cv, make new cv
    # He clicks make new cv
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/")
        start_new_cv_button = self.browser.find_element_by_id('start_new_cv')
        edit_existing_cv_button = self.browser.find_element_by_id('view_existing_cv')
        start_new_cv_button.click()
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/personal_details")

    # He finds the personal details section and inputs his data and hits next
        self.browser.find_element_by_id('id_first_name').send_keys("George")
        self.browser.find_element_by_id('id_last_name').send_keys("Kirkman")
        self.browser.find_element_by_id('id_profession').send_keys("Student")
        self.browser.find_element_by_id('id_city').send_keys("Watford")
        self.browser.find_element_by_id('id_postcode').send_keys("AB1 2CD")
        self.browser.find_element_by_id('id_phone_number').send_keys("+447847133344")
        self.browser.find_element_by_id('id_email').send_keys("george.kirkman27@gmail.com")
        self.browser.find_element_by_id('personal_details_next').click()

        self.fail("finish the test!")

    # Next is a short profile summary, some kind of char limit here

    # Next is the education section, where he enters his uni details

    # Next is work history, he enters the most recent employer details

    # He has to enter some details/description of the job on the next page (richtext editor)

    # He has the opporunity to add another, and takes it

    # Job2 work history, Job2 work description

    # Next page offers optional additions, user chooses to add skills

    # Add skills form, optional skill descriptions ? and ratings of proficiency

    # Back on the additional extras, now he picks interests and fills out some interests

    # Finally, back on the additional extras he has no more to add, and hits "finish" 

    # He is met with a formatted version of his cv (NOTE: exportable to pdf if possible!)