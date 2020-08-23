from django.test import Client #, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
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
        self.browser.find_element_by_id('submit-id-personal_details_next').click()

    # Next is a short profile summary, some kind of char limit here
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/profile")
        self.browser.find_element_by_class_name("ck-content").send_keys("This is my profile bio lorem ipsum cheeki breeki iv\
 damke pogchampion my duderino. That's my secret, captain, I'm always angry. How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.browser.find_element_by_id('profile_next').click()

    # Next is the education section, where he enters his uni details and then clicks "save and add another"
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("University of Birmingham")
        self.browser.find_element_by_id('id_location').send_keys("Birmingham")
        self.browser.find_element_by_id('id_subject').send_keys("BSc Computer Science")
        self.browser.find_element_by_id('id_grade').send_keys("First")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/09/2018")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/04/2021")
        self.browser.find_element_by_id('submit-id-education_save_and_add').click()
        
    # He also enters his A Levels
        # Chemistry 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Chemistry")
        self.browser.find_element_by_id('id_grade').send_keys("B")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/09/2015")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/04/2016")
        self.browser.find_element_by_id('submit-id-education_save_and_add').click()

        # Physics 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Physics")
        self.browser.find_element_by_id('id_grade').send_keys("A")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/09/2015")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/04/2016")
        self.browser.find_element_by_id('submit-id-education_save_and_add').click()

        # Maths 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_subject').send_keys("Mathematics")
        self.browser.find_element_by_id('id_grade').send_keys("A")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/09/2015")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/04/2016")
        self.browser.find_element_by_id('submit-id-education_next').click()

    # Next is work history, he enters the most recent employer details
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/work_history")
        self.browser.find_element_by_id('id_job_title').send_keys("Visitor Experience Helper")
        self.browser.find_element_by_id('id_employer').send_keys("The Science Museum")
        self.browser.find_element_by_id('id_city').send_keys("London")
        self.browser.find_element_by_class_name('ck-content').send_keys("I worked as a volunteer in the “Visitor Experience” team for the Science Museum’s Power Up exhibition."
            + Keys.ENTER + "1. Recounting the history of video-gaming to any interested visitors and discussing any areas of the history of the games and esports industry."
            + Keys.ENTER + "2. Helping parents and their children to connect by translating the child's passion and gaming experience into more understandable terms for the parents."
            + Keys.ENTER + "3. Introducing visitors to consoles or games they have never seen before and teaching their significance in the development of the industry.")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/04/2016")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("23/04/2016")
        self.browser.find_element_by_id('submit-id-work_history_save_and_add').click()

    # He has to enter some details/description of the job on the next page (richtext editor) TODO: currently on previous page, does it need separation?

    # He has the opporunity to add another, and takes it
        self.browser.find_element_by_id('id_job_title').send_keys("Sales Representative")
        self.browser.find_element_by_id('id_employer').send_keys("Three")
        self.browser.find_element_by_id('id_city').send_keys("Watford")
        self.browser.find_element_by_class_name('ck-content').send_keys("I worked as a part of the sales team in the Three mobile carrier shop in the high street's shopping centre." 
            + Keys.ENTER + "1. Curabitur eleifend arcu quis neque vehicula dapibus."
            + Keys.ENTER + "2. Duis hendrerit lectus ut eleifend tincidunt."
            + Keys.ENTER + "3. Maecenas et massa congue, pharetra nibh vitae, ultricies augue."
            + Keys.ENTER + "4. Integer sit amet est id lectus ornare vestibulum eget ac ipsum.")
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("19/07/2017")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/09/2017")
        self.browser.find_element_by_id('submit-id-work_history_next').click()

    # Next page offers optional additions, user chooses to add skills, interests, languages and certifications (all of em)
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/extras")
        self.browser.find_element_by_xpath('/html/body/div/div/div/form/div[1]/div/label').click() # Skills
        self.browser.find_element_by_xpath('/html/body/div/div/div/form/div[2]/div/label').click() # Interests
        self.browser.find_element_by_xpath('/html/body/div/div/div/form/div[3]/div/label').click() # Languages
        self.browser.find_element_by_xpath('/html/body/div/div/div/form/div[4]/div/label').click() # Certifications
        self.browser.find_element_by_id('submit-id-extras_next').click()

    # Add skills form, optional skill descriptions ? and ratings of proficiency?
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/skills")
        self.browser.find_element_by_id('id_skill').send_keys("Scuba")
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/div[2]/div/div/div[2]/div').send_keys("I can scuba!") # Description
        self.browser.find_element_by_id('submit-id-skill_add_another').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/skills")
        self.browser.find_element_by_id('id_skill').send_keys("Piano")
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/div[2]/div/div/div[2]/div').send_keys("Grade 8 piano") # Description
        self.browser.find_element_by_id('submit-id-skill_next').click()

    # Hitting next automatically sends him to the interests page
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/interests")
        self.browser.find_element_by_id('id_interest').send_keys("Gaming")
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/div[2]/div/div/div[2]/div').send_keys("Imma gamer") # Description
        self.browser.find_element_by_id('submit-id-interest_add_another').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/interests")
        self.browser.find_element_by_id('id_interest').send_keys("Technology")
        self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/div[2]/div/div/div[2]/div').send_keys("I like to keep up with the latest in gadgets.") # Description
        self.browser.find_element_by_id('submit-id-interest_next').click()

        # Hitting next automatically sends him to the languages page
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/languages")
        self.browser.find_element_by_id('id_language').send_keys("French")
        Select(self.browser.find_element_by_id('id_proficiency')).select_by_value('4')
        self.browser.find_element_by_id('submit-id-language_add_another').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/languages")
        self.browser.find_element_by_id('id_language').send_keys("German")
        Select(self.browser.find_element_by_id('id_proficiency')).select_by_value('3')
        self.browser.find_element_by_id('submit-id-language_next').click()

    # Hitting next takes him to certifications
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/certifications")
        self.browser.find_element_by_id('id_certification').send_keys("Insomnia 64 PUBG Solos Golden Pan Winner")
        date = self.browser.find_element_by_id('id_date')
        for x in range(10):
            date.send_keys(Keys.BACKSPACE)
        date.send_keys("19/07/2017")
        self.browser.find_element_by_xpath("//body").click() # NOTE: NOT NECESSARY AS I MOVED SUBMIT BUTTON, BUT THIS IS HOW TO CLICK "OFF" THE ELEMENT so it's not in the way
        self.browser.find_element_by_id('submit-id-certification_add_another').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/certifications")
        self.browser.find_element_by_id('id_certification').send_keys("Piano Grade 3")
        date = self.browser.find_element_by_id('id_date')
        for x in range(10):
            date.send_keys(Keys.BACKSPACE)
        date.send_keys("19/07/2010")
        self.browser.find_element_by_id('submit-id-certification_next').click()
        self.fail("finish the test!")

    # He is met with a formatted version of his cv (NOTE: exportable to pdf if possible!)