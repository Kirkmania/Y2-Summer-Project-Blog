from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string

# Create your tests here.
class CVUnitTests(TestCase):
    def test_cv_html_returned(self):
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response, 'online_cv/cv.html')

    