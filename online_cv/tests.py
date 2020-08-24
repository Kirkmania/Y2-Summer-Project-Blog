from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.template.loader import render_to_string
from .forms import cvPersonalDetailsForm, cvProfileForm, cvEducationForm, cvWorkHistoryForm, cvExtrasForm, cvSkillForm, cvInterestForm, cvCertificationForm, cvLanguageForm
from .models import cvSkill
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
            "level_of_study": "A Level",
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
        self.assertEqual(cv_education.level_of_study, "A Level")
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

    def test_extras_is_saved_and_redirects_correctly(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvExtrasForm({
            "skills": True, 
            "interests": True, 
            "certifications": True, 
            })

        self.assertTrue(form.is_valid())
        cv_extras = form.save(commit=False)
        cv_extras.user = self.user
        cv_extras.save()
        self.assertEqual(cv_extras.skills, True)
        self.assertEqual(cv_extras.interests, True)
        self.assertEqual(cv_extras.languages, False)
        self.assertEqual(cv_extras.certifications, True)

        # Should redirect to skills when no skills exist
        response = c.get('/cv/extras')
        self.assertRedirects(response, '/cv/skills')

        # When skills object(s) exist, should redirect to interests
        response = c.post('/cv/skills', {'skill': 'Programming', 'description': 'I can code'})
        self.assertRedirects(response, '/cv/interests')

        # When interest object(s) exist, should redirect to certs
        response = c.post('/cv/interests', {'interest': 'Programming', 'description': 'I like code'})
        self.assertRedirects(response, '/cv/certifications')

    def test_skills_are_correctly_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvSkillForm({
            "skill": "Scuba", 
            "description": "I can scuba", 
            })
        
        self.assertTrue(form.is_valid())
        cv_skill = form.save(commit=False)
        cv_skill.user = self.user
        cv_skill.save()

        form2 = cvSkillForm({
            "skill": "Diving", 
            "description": "I can dive!", 
            })

        self.assertTrue(form2.is_valid())
        cv_skill2 = form2.save(commit=False)
        cv_skill2.user = self.user
        cv_skill2.save()

        self.assertEqual(cv_skill.skill, "Scuba")
        self.assertEqual(cv_skill.description, "I can scuba")
        self.assertEqual(cv_skill2.skill, "Diving")
        self.assertEqual(cv_skill2.description, "I can dive!")

    def test_interest_is_correctly_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvInterestForm({
            "interest": "Esports", 
            "description": "Who's more popular, Shroud or Faker?", 
            })
        
        self.assertTrue(form.is_valid())
        cv_interest = form.save(commit=False)
        cv_interest.user = self.user
        cv_interest.save()

        self.assertEqual(cv_interest.interest, "Esports")
        self.assertEqual(cv_interest.description, "Who's more popular, Shroud or Faker?")

    def test_certification_is_correctly_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvCertificationForm({
            "date": "23/09/2018", 
            "certification": "Certification name", 
            })
        
        self.assertTrue(form.is_valid())
        cv_certification = form.save(commit=False)
        cv_certification.user = self.user
        cv_certification.save()

        self.assertEqual(cv_certification.date, datetime.date(2018, 9, 23))
        self.assertEqual(cv_certification.certification, "Certification name")

    def test_language_is_correctly_saved(self):
        c = self.client
        login = c.login(username="username", password="password")
        self.assertTrue(login)

        form = cvLanguageForm({
            "language": "French", 
            "proficiency": "3", 
            })
        
        self.assertTrue(form.is_valid())
        cv_language = form.save(commit=False)
        cv_language.user = self.user
        cv_language.save()

        self.assertEqual(cv_language.language, "French")
        self.assertEqual(cv_language.proficiency, "3")