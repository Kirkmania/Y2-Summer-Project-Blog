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

    # Next is a short profile summary, some kind of char limit here
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/profile")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("This is my profile bio lorem ipsum cheeki breeki iv\
 damke pogchampion my duderino. That's my secret, captain, I'm always angry. How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.browser.switch_to_default_content()
        self.browser.find_element_by_id('profile_next').click()

    # Next is the education section, where he enters his uni details and then clicks "save and add another"
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("University of Birmingham")
        self.browser.find_element_by_id('id_school_location').send_keys("Birmingham")
        self.browser.find_element_by_id('id_subject').send_keys("BSc Computer Science")
        self.browser.find_element_by_id('id_grade').send_keys("First")
        self.browser.find_element_by_id('id_start_date').send_keys("23092018")
        self.browser.find_element_by_id('id_end_date').send_keys("15042021")
        self.browser.find_element_by_id('education_save_and_add')
    
    # He also enters his A Levels
        # Chemistry 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_school_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Chemistry")
        self.browser.find_element_by_id('id_grade').send_keys("B")
        self.browser.find_element_by_id('id_start_date').send_keys("23092015")
        self.browser.find_element_by_id('id_end_date').send_keys("15042016")
        self.browser.find_element_by_id('education_save_and_add')

        # Physics 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_school_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Physics")
        self.browser.find_element_by_id('id_grade').send_keys("A")
        self.browser.find_element_by_id('id_start_date').send_keys("23092015")
        self.browser.find_element_by_id('id_end_date').send_keys("15042016")
        self.browser.find_element_by_id('education_save_and_add')

        # Maths 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_school_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Mathematics")
        self.browser.find_element_by_id('id_grade').send_keys("A")
        self.browser.find_element_by_id('id_start_date').send_keys("23092015")
        self.browser.find_element_by_id('id_end_date').send_keys("15042016")
        self.browser.find_element_by_id('education_save_and_add')

    # Next is work history, he enters the most recent employer details
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/work_history")
        self.browser.find_element_by_id('id_job_title').send_keys("Visitor Experience Helper")
        self.browser.find_element_by_id('id_employer').send_keys("The Science Museum")
        self.browser.find_element_by_id('id_city').send_keys("London")
        self.browser.find_element_by_id('id_description').send_keys("I worked as a volunteer in the “Visitor Experience” team for the Science Museum’s Power Up exhibition.\
            • Recounting the history of video-gaming to any interested visitors and discussing any areas of the history of the games and esports industry.\
            • Helping parents and their children to connect by translating the child's passion and gaming experience into more understandable terms for the parents.\
            • Introducing visitors to consoles or games they have never seen before and teaching their significance in the development of the industry.")
        self.browser.find_element_by_id('id_start_date').send_keys("23042016")
        self.browser.find_element_by_id('id_end_date').send_keys("23052016")
        self.browser.find_element_by_id('job_save_and_add')

    # He has to enter some details/description of the job on the next page (richtext editor) TODO: currently on previous page, does it need separation?

    # He has the opporunity to add another, and takes it
        self.browser.find_element_by_id('id_job_title').send_keys("Sales Representative")
        self.browser.find_element_by_id('id_employer').send_keys("Three")
        self.browser.find_element_by_id('id_city').send_keys("Watford")
        self.browser.find_element_by_id('id_description').send_keys("I worked as a part of the sales team in the Three mobile carrier shop in the high street's shopping centre.\
            • Curabitur eleifend arcu quis neque vehicula dapibus.\
            • Duis hendrerit lectus ut eleifend tincidunt.\
            • Maecenas et massa congue, pharetra nibh vitae, ultricies augue.\
            • Integer sit amet est id lectus ornare vestibulum eget ac ipsum.")
        self.browser.find_element_by_id('id_start_date').send_keys("19072017")
        self.browser.find_element_by_id('id_end_date').send_keys("15092017")
        self.browser.find_element_by_id('job_save_and_next')

    # Next page offers optional additions, user chooses to add skills
        self.fail("finish the test!")
    # Add skills form, optional skill descriptions ? and ratings of proficiency

    # Back on the additional extras, now he picks interests and fills out some interests

    # Finally, back on the additional extras he has no more to add, and hits "finish" 

    # He is met with a formatted version of his cv (NOTE: exportable to pdf if possible!)