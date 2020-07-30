from django.test import LiveServerTestCase, Client
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from blog.models import Post
from django.utils import timezone
import time
#import unittest

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

        test = Post.objects.create(author=self.user_admin, title="Hipster Ipsum", text="I'm baby glossier pug gastropub yr woke photo booth.\
             Whatever umami enamel pin synth organic art party raw denim church-key. Jianbing lyft selvage pabst, \
            poutine ugh four dollar toast. Kale chips umami thundercats man bun street art truffaut pork belly mixtape distillery hoodie polaroid occupy. \
            Vegan tacos occupy ethical, craft beer master cleanse crucifix tbh banh mi sartorial activated charcoal snackwave.",
        created_date="2020-07-28 20:50", published_date="2020-07-28 20:51")
        test.save()

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

        # He enters his username and password, confirming his new account
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
        # After submitting his signup he returns to the homepage and sees the latest post
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

        # Upon returning to the home page, he clicks the new "new post" button and writes a blog post
        self.browser.find_element_by_id('post_new_button').click()

        newpost_title = self.browser.find_element_by_id('id_title')
        newpost_text = self.browser.find_element_by_id('id_text')
        post_save_button = self.browser.find_element_by_id('save_post')

        newpost_title.send_keys('Lorem Ipsum')  # Hey cool, this \ thing lets you overflow strings in python!
        newpost_text.send_keys('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ac ex ante. \
            Nullam iaculis fermentum tortor, non suscipit elit aliquet quis. Donec consequat placerat accumsan. \
            Praesent et ante non mi finibus pellentesque sed eget metus. In posuere, massa vel aliquet elementum, \
            metus nisi interdum tellus, in accumsan sapien ex vitae neque. Aliquam viverra in magna vitae fringilla. \
            Curabitur a scelerisque neque. Ut tortor nisi, posuere sit amet neque a, viverra congue ligula. \
            Maecenas in porta ligula. Nam lobortis commodo diam, id ultrices libero ullamcorper aliquam. \
            Quisque consectetur leo ante, id tincidunt erat semper sit amet. In pellentesque feugiat iaculis. \
            Ut sit amet ante facilisis, auctor neque a, tincidunt libero. Pellentesque ut varius lorem, in luctus sapien. \
            Praesent ullamcorper ante eget magna maximus accumsan. ')

        post_save_button.click()

        # He wants to check his other drafts first before he publishes, so clicks to homepage, then "drafts" button
        self.browser.find_element_by_link_text("George's Blog").click()
        self.browser.find_element_by_id('post_drafts_button').click()
        self.browser.find_element_by_link_text('Lorem Ipsum').click()

        # He notices a missing line to add before publishing
        self.browser.find_element_by_id('post_edit').click()

        newpost_title = self.browser.find_element_by_id('id_title')
        newpost_text = self.browser.find_element_by_id('id_text')
        post_save_button = self.browser.find_element_by_id('save_post')

        newpost_text.send_keys(' This is my missing line!')
        post_save_button.click()

        # He happily publishes his new blogpost!
        self.browser.find_element_by_id('post_publish').click()
        published_post = Post.objects.get(title="Lorem Ipsum")
        self.assertIsNotNone(published_post.published_date)

        # The post is now visible from the homepage blog post list
        self.browser.find_element_by_link_text("George's Blog").click()


        # NOTE FINISH THE STORY!

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