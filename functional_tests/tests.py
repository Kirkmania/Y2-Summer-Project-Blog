from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
#import unittest

########## NOTE DON'T KEEP ?? NOT LIVE SERVER CASE
from django.test import override_settings
@override_settings(DEBUG=True)


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        #create permissions group
        self.group_admin = Group(name="admin")
        self.group_admin.save()
        self.group_newcomer = Group(name="newcomer")
        self.group_newcomer.save()

        self.user_admin = User.objects.create_superuser(
            username='test',
            password='test',
            email='test@test.com',
        )

        self.user_admin.groups.add(self.group_admin)

    def tearDown(self):
        self.browser.quit()

    # helper function for testing row text!
    # https://www.obeythetestinggoat.com/book/chapter_post_and_database.html
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    def test_user_can_see_blog_posts_and_signup(self):
        # George has started along the Way of the Testing Goat and
        # pretends to check out a new blog
        self.browser.get(self.live_server_url)

        # He notices the page title and header mentions a blog
        self.assertIn('Blog', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Blog', header_text)

        # He clicks on the sign-up button and is taken to a sign-up page
        signup_button = self.browser.find_element_by_id('signup_button')
        signup_button.click()

        time.sleep(1)  #NOTE REPLACE VODOO SLEEPS!

        # He enters his username and password, confirming his new account (let's make it admin too)
        signup_username = self.browser.find_element_by_id('id_username')
        signup_password1 = self.browser.find_element_by_id('id_password1')
        signup_password2 = self.browser.find_element_by_id('id_password2')
        signup_submit_button = self.browser.find_element_by_id('signup_submit')

        signup_username.send_keys('Jane_Doe')
        signup_password1.send_keys('DjangoTest123')
        signup_password2.send_keys('DjangoTest123')
        signup_submit_button.click()

        time.sleep(3) #NOTE REPLACE VOODOO SLEEPS!
        self.fail('Is this the end?!')

        #NOTE NEED TO ADD A POST BEFORE THIS!
        post_text = self.browser.find_element_by_class_name('post').text
        self.assertIn('Hello yes I am blog continue', post_text, 'this probably wont work')

    def test_admin_user_can_create_and_view_posts(self):
        self.browser.get(self.live_server_url)

        login_button = self.browser.find_element_by_id('login_button')
        login_button.click()

        time.sleep(1)

        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')
        signup_submit_button = self.browser.find_element_by_id('login_submit')

        login_username.send_keys('test')
        login_password.send_keys('test')
        signup_submit_button.click()

        time.sleep(1)

        self.browser.find_element_by_id('post_new_button').click()
        time.sleep(5)
        # Upon returning to the home page, he finds some new buttons available to him
        

        # He presses the new blog post button and finds a post submission form

        # He fills in his post details and saves it as a draft

        # Refreshing the page (?) he sees a publish button which he presses

        # The post is now visible from the homepage blog post list

        # NOTE FINISH THE STORY!

        # NOTE INCLUDE THIS LATER! He is invited to enter a to-do item pronto


#################################################################################################################### OLD STUFF
        # inputbox = self.browser.find_element_by_id('id_new_item')
        # self.assertEqual(
        #     inputbox.get_attribute('placeholder'),
        #     'Enter a to-do item'
        # )

        # # He types "Play more Call of Duty" into a text box
        # inputbox.send_keys('Play more Call of Duty')

        # # When he hits enter, the page updates, and now the page lists
        # # "1: Play more Call of Duty" as an item in a to-do list NOTE: Cool stuff used to be here. f-string and any() function
        # inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)
        # self.check_for_row_in_list_table('1: Play more Call of Duty')

        # # There is still a text box inviting him to to add another item.
        # # He enters "Make the blog look prettier"
        # inputbox = self.browser.find_element_by_id('id_new_item')
        # inputbox.send_keys('Make the blog look prettier')
        # inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        # # The page updates again, and now shows both items on her list
        # self.check_for_row_in_list_table('1: Play more Call of Duty')
        # self.check_for_row_in_list_table('2: Make the blog look prettier')

        # # George wonders whether the site will remember his list. Then he sees
        # # that the site has generated a unique URL for him, with some explanatory
        # # text to that effect.
        # self.fail('Finish the test!')

        # # He visits that URL, his to-do list is still there.

        # # Satisfied, he goes back to sleep.

# if __name__ == '__main__':
#    unittest.main()             # Not needed anymore