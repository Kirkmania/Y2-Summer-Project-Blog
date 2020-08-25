from django.test import Client #, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        self.client.login(username='Kassandra', password='malaka')

    def tearDown(self):
        self.browser.quit()

    def test_user_can_see_blog_posts_and_signup(self):
        self.browser.get(self.live_server_url)
        # INCREASE THIS CONSTANT if buttons are obscured by backdrops
        # I'm sorry I was naughty and used time.sleep(), I promise I went to 5 different stack overflows
        # all struggling over WebDriverWait until EC element is invisible/not present/etc and not managing to get them to work
        # with modal dialogs with javascript fade animations!!!
        MODAL_HIDE_TIME = 0.3

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
        self.browser.find_element_by_id('start_new_cv_confirm').click()
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/personal_details")

    # He finds the personal details section and inputs his data and hits next
        time.sleep(MODAL_HIDE_TIME)
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
        self.browser.find_element_by_id('id_add_education').click()
        self.browser.find_element_by_id('id_school').send_keys("University of Birmingham")
        self.browser.find_element_by_id('id_location').send_keys("Birmingham")
        self.browser.find_element_by_id('id_level_of_study').send_keys("BSc Degree")
        self.browser.find_element_by_id('id_subject').send_keys("Computer Science")
        start_date = self.browser.find_element_by_id('id_start_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/09/2018")
        self.browser.find_element_by_class_name('modal-header').click()  
        self.browser.find_element_by_id('id_confirm_education').click()

    # He also enters his A Levels
        # Chemistry 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        # I AM SORRY BUT I AM USING EXPLICIT SLEEPS HERE. :(
        # For context, I attempted to use the following piece of wait code and many variations of it. It "worked", but actually took much longer than a 1 second delay would.
        # WebDriverWait(self.browser, 5).until_not(EC.presence_of_element_located((By.CLASS_NAME, "modal-backdrop fade show")))
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_education').click()
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_level_of_study').send_keys("A Level")
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
        self.browser.find_element_by_class_name('modal-header').click() 
        self.browser.find_element_by_id('id_confirm_education').click()

        # Physics 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_education').click()
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_level_of_study').send_keys("A Level")
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
        self.browser.find_element_by_class_name('modal-header').click()
        self.browser.find_element_by_id('id_confirm_education').click()

        # Maths 
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/education")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_education').click()
        self.browser.find_element_by_id('id_school').send_keys("Rickmansworth 6th Form")
        self.browser.find_element_by_id('id_location').send_keys("Watford")
        self.browser.find_element_by_id('id_level_of_study').send_keys("A Level")
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
        self.browser.find_element_by_class_name('modal-header').click()
        self.browser.find_element_by_id('id_confirm_education').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_next').click()

    # Next is work history, he enters the most recent employer details
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/jobs")
        self.browser.find_element_by_id('id_add_job').click()
        self.browser.find_element_by_id('id_job_title').send_keys("Visitor Experience Helper")
        self.browser.find_element_by_id('id_employer').send_keys("The Science Museum")
        self.browser.find_element_by_id('id_city').send_keys("London")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("I worked as a volunteer in the “Visitor Experience” team for the Science Museum’s Power Up exhibition.")
        self.browser.switch_to_default_content()
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("23/04/2016")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("23/04/2016")
        self.browser.find_element_by_class_name('modal-header').click()
        self.browser.find_element_by_id('id_confirm_job').click()

    # He has the opporunity to add another, and takes it
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_job').click()
        self.browser.find_element_by_id('id_job_title').send_keys("Sales Representative")
        self.browser.find_element_by_id('id_employer').send_keys("Three")
        self.browser.find_element_by_id('id_city').send_keys("Watford")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("I worked as a part of the sales team in the Three mobile carrier shop in the high street's shopping centre.")
        self.browser.switch_to_default_content()
        start_date = self.browser.find_element_by_id('id_start_date')
        end_date = self.browser.find_element_by_id('id_end_date')
        for x in range(10):
            start_date.send_keys(Keys.BACKSPACE)
        start_date.send_keys("19/07/2017")
        for x in range(10):
            end_date.send_keys(Keys.BACKSPACE)
        end_date.send_keys("15/09/2017")
        self.browser.find_element_by_id('id_confirm_job').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id("id_next").click()

    # Next page offers optional additions, user chooses to add skills, interests, languages and certifications (all of em)
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/extras")
        self.browser.find_element_by_xpath('//*[@id="div_id_skills"]/label').click() # Skills
        self.browser.find_element_by_xpath('//*[@id="div_id_interests"]/label').click() # Interests
        self.browser.find_element_by_xpath('//*[@id="div_id_languages"]/label').click() # Languages
        self.browser.find_element_by_xpath('//*[@id="div_id_certifications"]/label').click() # Certifications
        self.browser.find_element_by_id('submit-id-extras_next').click()

    # Add skills form, optional skill descriptions ? and ratings of proficiency?
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/skills")
        self.browser.find_element_by_id('id_add_skill').click()
        self.browser.find_element_by_id('id_skill').send_keys("Scuba")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("I can scuba!") # Description
        self.browser.switch_to_default_content()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_skill').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/skills")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_skill').click()
        self.browser.find_element_by_id('id_skill').send_keys("Piano")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("Grade 8 piano")
        self.browser.switch_to_default_content()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_skill').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id("id_next").click()

    # Hitting next automatically sends him to the interests page
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/interests")
        self.browser.find_element_by_id('id_add_interest').click()
        self.browser.find_element_by_id('id_interest').send_keys("Gaming")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("Imma gamer")
        self.browser.switch_to_default_content()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_interest').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/interests")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_interest').click()
        self.browser.find_element_by_id('id_interest').send_keys("Technology")
        self.browser.switch_to_frame(self.browser.find_element_by_tag_name('iframe'))
        self.browser.find_element_by_class_name("cke_editable").send_keys("I like to keep up with the latest in gadgets.")
        self.browser.switch_to_default_content()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_interest').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id("id_next").click()

        # Hitting next automatically sends him to the languages page
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/languages")
        self.browser.find_element_by_id('id_add_language').click()
        self.browser.find_element_by_id('id_language').send_keys("French")
        Select(self.browser.find_element_by_id('id_proficiency')).select_by_value('Full Professional')
        self.browser.find_element_by_id('id_confirm_language').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/languages")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_language').click()
        self.browser.find_element_by_id('id_language').send_keys("German")
        Select(self.browser.find_element_by_id('id_proficiency')).select_by_value('Elementary')
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_language').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id("id_next").click()

    # Hitting next takes him to certifications
        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/certifications")
        self.browser.find_element_by_id('id_add_certification').click()
        self.browser.find_element_by_id('id_certification').send_keys("Insomnia 64 PUBG Solos Golden Pan Winner")
        date = self.browser.find_element_by_id('id_date')
        for x in range(10):
            date.send_keys(Keys.BACKSPACE)
        date.send_keys("19/07/2017")
        #self.browser.find_element_by_xpath("//body").click() # NOTE: NOT NECESSARY AS I MOVED SUBMIT BUTTON, BUT THIS IS HOW TO CLICK "OFF" THE ELEMENT so it's not in the way
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_certification').click()

        self.assertURLEqual(self.browser.current_url, self.live_server_url + "/cv/certifications")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_add_certification').click()
        self.browser.find_element_by_id('id_certification').send_keys("Piano Grade 3")
        date = self.browser.find_element_by_id('id_date')
        for x in range(10):
            date.send_keys(Keys.BACKSPACE)
        date.send_keys("19/07/2010")
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_confirm_certification').click()
        time.sleep(MODAL_HIDE_TIME)
        self.browser.find_element_by_id('id_next').click()

    # BIG CHECK TIME let's see if all the text George filled in is present!
        response = self.client.get('/cv/preview')
        self.browser
        self.assertContains(response, "This is my profile bio lorem ipsum cheeki breeki iv damke pogchampion my duderino. That's my secret, captain, I'm always angry. How much wood could a woodchuck chuck if a woodchuck could chuck wood?")
        self.assertContains(response,"Scuba")
        self.assertContains(response,"I can scuba!")
        self.assertContains(response,"Gaming")
        self.assertContains(response,"Imma gamer")
        self.assertContains(response,"French")
        self.assertContains(response,"Full Professional")
        self.assertContains(response,"Piano Grade 3")
        self.assertContains(response,"19 Jul 2010")
        self.assertContains(response,"BSc Degree: Computer Science (currently studying) at University of Birmingham, Birmingham")
        self.assertContains(response,"<strong>Visitor Experience Helper</strong>, The Science Museum, London")
        self.assertContains(response,"I worked as a volunteer in the &ldquo;Visitor Experience&rdquo; team for the Science Museum&rsquo;s Power Up exhibition.")
        self.fail("finish the test!")

    # He is met with a formatted version of his cv (NOTE: exportable to pdf if possible!)