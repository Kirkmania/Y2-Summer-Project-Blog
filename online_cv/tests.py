from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from .forms import cvPersonalDetailsForm, cvProfileForm

# Create your tests here.
class CVUnitTests(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='username',
            password='password',
            email='test1@test1.com',
        )

    def test_cv_html_returned(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        response = c.get('/cv/')
        self.assertTemplateUsed(response, 'online_cv/cv_builder.html')

    def test_person_details_are_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvPersonalDetailsForm({
            "first_name": "George", 
            "last_name": "Kirkman", 
            "profession": "Student", 
            "city": "Watford", 
            "postcode": "AB1 2CD", 
            "phone_number": "+447847133344", 
            "email": "george.kirkman27@gmail.com", })

        self.assertTrue(form.is_valid())
        cv_personal_details = form.save(commit=False)
        cv_personal_details.user = self.user
        cv_personal_details.save()
        self.assertEqual(cv_personal_details.first_name, "George")
        self.assertEqual(cv_personal_details.last_name, "Kirkman")
        self.assertEqual(cv_personal_details.profession, "Student")
        self.assertEqual(cv_personal_details.city, "Watford")
        self.assertEqual(cv_personal_details.postcode, "AB1 2CD")
        self.assertEqual(cv_personal_details.phone_number, "+447847133344")
        self.assertEqual(cv_personal_details.email, "george.kirkman27@gmail.com")

    def test_profile_is_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvProfileForm({"text": "<p>This is some example profile text.</p>",})

        self.assertTrue(form.is_valid())
        cv_profile = form.save(commit=False)
        cv_profile.user = self.user
        self.assertEqual(cv_profile.text, "<p>This is some example profile text.</p>")