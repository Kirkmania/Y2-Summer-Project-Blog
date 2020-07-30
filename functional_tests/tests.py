from django.test import Client #, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import Group, User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from blog.models import Post, Comment
from django.utils import timezone
import time
#import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

        #create permissions group
        self.group_admin = Group(name="admin")
        self.group_admin.save()
        self.group_newcomer = Group(name="newcomer")
        self.group_newcomer.save()

        self.user_admin = User.objects.create_superuser(
            username='Hipster',
            password='starbucks',
            email='test@test.com',
        )

        self.user = User.objects.create_user(
            username='Kassandra',
            password='malaka',
            email='test1@test1.com',
        )

        self.user_admin.groups.add(self.group_admin)
        self.user.groups.add(self.group_newcomer)

        post = Post.objects.create(author=self.user_admin, title="Hipster Ipsum", text="I'm baby glossier pug gastropub yr woke photo booth.\
             Whatever umami enamel pin synth organic art party raw denim church-key. Jianbing lyft selvage pabst, \
            poutine ugh four dollar toast. Kale chips umami thundercats man bun street art truffaut pork belly mixtape distillery hoodie polaroid occupy. \
            Vegan tacos occupy ethical, craft beer master cleanse crucifix tbh banh mi sartorial activated charcoal snackwave.",
        created_date="2020-07-28 20:50", published_date="2020-07-28 20:51")

        comment_approved = Comment.objects.create(post=post,
            author=self.user_admin,
            text="Does this work??",
            created_date="2020-07-28 20:51",
            approved_comment=True)

        comment = Comment.objects.create(post=post,
            author=self.user,
            text="I've HAD it with those damn Kosmos Cultists!!",
            created_date="0001-05-23 18:38")

        post.save()


        
    def tearDown(self):
        self.browser.quit()

    # helper function for testing row text!
    # https://www.obeythetestinggoat.com/book/chapter_post_and_database.html
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    ### Test Number 1 ###
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

        # He enters his username and password, confirming his new account
        signup_username = self.browser.find_element_by_id('id_username')
        signup_password1 = self.browser.find_element_by_id('id_password1')
        signup_password2 = self.browser.find_element_by_id('id_password2')
        signup_submit_button = self.browser.find_element_by_id('signup_submit')

        signup_username.send_keys('Jane_Doe')
        signup_password1.send_keys('DjangoTest123')
        signup_password2.send_keys('DjangoTest123')
        signup_submit_button.click()

        # time.sleep(1) #NOTE REPLACE VOODOO SLEEPS!

        # After signing up he is redirected to the homepage and sees the latest post
        post = self.browser.find_element_by_class_name('post')
        # self.assertIn("baby glossier pug gastropub", [post.text for post in posts]) doesn't work for some reason?
        self.assertIn("baby glossier pug gastropub", post.text)
        time.sleep(10)

    ### Test Number 2 ###
    def test_admin_user_can_create_and_view_posts(self):
        self.browser.get(self.live_server_url)

        # Mr admin user wants to log in to the site
        login_button = self.browser.find_element_by_id('login_button')
        login_button.click()
        
        # He enters his username, password and hits submit
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')
        login_submit_button = self.browser.find_element_by_id('login_submit')

        login_username.send_keys('Hipster')
        login_password.send_keys('starbucks')
        login_submit_button.click()

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

        # He wants to check his other drafts first before he publishes, so clicks back to homepage, then "drafts" button
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

        # Missing line has been added
        edited_post = Post.objects.get(title="Lorem Ipsum")
        self.assertIn("This is my missing line!", edited_post.text)

        # He happily publishes his new blogpost!
        self.browser.find_element_by_id('post_publish').click()
        published_post = Post.objects.get(title="Lorem Ipsum")
        self.assertIsNotNone(published_post.published_date)

        # The post is now visible from the homepage blog post list
        self.browser.find_element_by_link_text("George's Blog").click()
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("Lorem Ipsum", body_text)

    def test_user_can_view_and_admin_moderate_comments(self):
        self.browser.get(self.live_server_url)

        # Mr admin user logs in to the site
        login_button = self.browser.find_element_by_id('login_button')
        login_button.click()
        
        # He enters his username, password and hits submit
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')
        login_submit_button = self.browser.find_element_by_id('login_submit')

        login_username.send_keys('Hipster')
        login_password.send_keys('starbucks')
        login_submit_button.click()

        # Back at the homepage, he checks out the latest post's comments
        self.browser.find_element_by_link_text("Hipster Ipsum").click()
        comments = self.browser.find_elements_by_class_name("comment")
        self.assertIn("Does this work??", comments[0].text)

        # He sees an new (very old) comment from Kassandra the assassin, which he approves
        self.assertIn("Kassandra", comments[1].text)
        self.browser.find_element_by_id("comment_approve").click()

        # Finally, let's try adding a new comment
        self.browser.find_element_by_id("comment_add").click()
        self.browser.find_element_by_id("id_author").send_keys('Hipster')
        self.browser.find_element_by_id("id_text").send_keys('MAN do I love my frapp-omegaccino with extra zest!')
        self.browser.find_element_by_id("comment_submit").click()
        self.browser.find_element_by_id("comment_approve").click()

        # Let's just make sure a non-admin user can see the comments!
        self.browser.find_element_by_link_text("Log out").click()
        
        login_button = self.browser.find_element_by_id('login_button')
        login_button.click()
        login_username = self.browser.find_element_by_id('id_username')
        login_password = self.browser.find_element_by_id('id_password')
        login_submit_button = self.browser.find_element_by_id('login_submit')
        login_username.send_keys('Kassandra')
        login_password.send_keys('malaka')
        login_submit_button.click()

        # Is the new comment visible?
        self.browser.find_element_by_link_text("Hipster Ipsum").click()
        comments = self.browser.find_elements_by_class_name("comment")
        self.assertIn("Kosmos Cultists", comments[1].text)

        # Admin's comment should also be visible
        self.assertIn("frapp-omegaccino", comments[2].text)

# if __name__ == '__main__':
#    unittest.main()             # Not needed anymore