from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from .forms import cvPersonalDetailsForm, cvProfileForm, cvEducationForm, cvWorkHistoryForm, cvExtrasForm
import datetime

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

    def test_education_is_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvEducationForm({
            "school": "Schoolname", 
            "location": "Schoolplace", 
            "subject": "Computer Science", 
            "grade": "First", 
            "start_date": "23/09/2018", 
            "end_date": "15/04/2021",
            })

        self.assertTrue(form.is_valid())
        cv_education = form.save(commit=False)
        cv_education.user = self.user
        cv_education.save()
        self.assertEqual(cv_education.school, "Schoolname")
        self.assertEqual(cv_education.location, "Schoolplace")
        self.assertEqual(cv_education.subject, "Computer Science")
        self.assertEqual(cv_education.grade, "First")
        self.assertEqual(cv_education.start_date, datetime.date(2018, 9, 23))
        self.assertEqual(cv_education.end_date, datetime.date(2021, 4, 15))

    def test_work_history_is_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvWorkHistoryForm({
            "job_title": "Jobname", 
            "employer": "Employername", 
            "city": "London", 
            "description": "<p>This is some example job text.</p>", 
            "start_date": "23/09/2018", 
            "end_date": "15/04/2019",
            })

        self.assertTrue(form.is_valid())
        cv_education = form.save(commit=False)
        cv_education.user = self.user
        cv_education.save()
        self.assertEqual(cv_education.job_title, "Jobname")
        self.assertEqual(cv_education.employer, "Employername")
        self.assertEqual(cv_education.city, "London")
        self.assertEqual(cv_education.description, "<p>This is some example job text.</p>")
        self.assertEqual(cv_education.start_date, datetime.date(2018, 9, 23))
        self.assertEqual(cv_education.end_date, datetime.date(2019, 4, 15))

    def test_extras_is_saved_and_redirects(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvExtrasForm({
            "skills": True, 
            "interests": True, 
            "languages": True, 
            })

        self.assertTrue(form.is_valid())
        cv_extras = form.save(commit=False)
        cv_extras.user = self.user
        cv_extras.save()
        self.assertEqual(cv_extras.skills, True)
        self.assertEqual(cv_extras.interests, True)
        self.assertEqual(cv_extras.languages, True)
        self.assertEqual(cv_extras.certifications, False)
        response = c.get('/cv/extras')
        self.assertRedirects(response, '/cv/skills')
        