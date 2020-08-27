from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string

from blog.models import Post

class HomePageTest(TestCase):
    def setUp(self):
        #create permissions groups
        self.group_admin = Group(name="admin")
        self.group_admin.save()
        self.group_newcomer = Group(name="newcomer")
        self.group_newcomer.save()

        self.user_admin = User.objects.create_superuser(
            username='admin',
            password='admin',
            email='test@test.com',
        )

        self.user = User.objects.create_user(
            username='user',
            password='user',
            email='test1@test1.com',
        )

        self.user_admin.groups.add(self.group_admin)
        self.user.groups.add(self.group_newcomer)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_can_save_a_POST_request(self):
        login = self.client.login(username="admin", password="admin")
        self.assertTrue(login)

        response = self.client.post('/post/new/', data={'title': "This is a test", 'category':'Testing', 'text': "I hope this test works"})

        self.assertEqual(Post.objects.count(), 1)
        new_post = Post.objects.first()
        self.assertEqual(new_post.text, 'I hope this test works')
