from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from .forms import cvPersonalDetailsForm

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
        cvPersonalDetails = form.save(commit=False)
        cvPersonalDetails.user = self.user
        self.assertEqual(cvPersonalDetails.first_name, "George")
        self.assertEqual(cvPersonalDetails.last_name, "Kirkman")
        self.assertEqual(cvPersonalDetails.profession, "Student")
        self.assertEqual(cvPersonalDetails.city, "Watford")
        self.assertEqual(cvPersonalDetails.postcode, "AB1 2CD")
        self.assertEqual(cvPersonalDetails.phone_number, "+447847133344")
        self.assertEqual(cvPersonalDetails.email, "george.kirkman27@gmail.com")