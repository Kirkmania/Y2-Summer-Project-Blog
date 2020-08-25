from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [  
    path('', views.cv_builder, name='cv_builder'),
    path('start_new', views.start_new, name='cv_start_new'),
    path('personal_details', views.personal_details, name='cv_personal_details'),
    path('profile', views.profile, name='cv_profile'),
    # path('education', views.education, name='cv_education'),
    # path('work_history', views.work_history, name='cv_work_history'),
    path('extras', views.extras, name='cv_extras'),
    path('extras/edit', views.extras_edit, name='cv_extras_edit'),
    path('certifications', views.certifications, name='cv_certifications'),
    path('preview', views.preview, name='cv_preview'),
    path('skills', views.skills, name='cv_skills'),
    path('skills/create', views.skill_create, name='cv_skill_create'),
    path('skills/<int:pk>/edit', views.skill_edit, name='cv_skill_edit'),
    path('skills/<int:pk>/delete', views.skill_delete, name='cv_skill_delete'),
    path('skills/next', views.skill_next, name='cv_skills_next'),
    path('interests', views.interests, name='cv_interests'),
    path('interests/create', views.interest_create, name='cv_interest_create'),
    path('interests/<int:pk>/edit', views.interest_edit, name='cv_interest_edit'),
    path('interests/<int:pk>/delete', views.interest_delete, name='cv_interest_delete'),
    path('interests/next', views.interest_next, name='cv_interests_next'),
    path('languages', views.languages, name='cv_languages'),
    path('languages/create', views.language_create, name='cv_language_create'),
    path('languages/<int:pk>/edit', views.language_edit, name='cv_language_edit'),
    path('languages/<int:pk>/delete', views.language_delete, name='cv_language_delete'),
    path('languages/next', views.language_next, name='cv_languages_next'),
    path('certifications', views.certifications, name='cv_certifications'),
    path('certifications/create', views.certification_create, name='cv_certification_create'),
    path('certifications/<int:pk>/edit', views.certification_edit, name='cv_certification_edit'),
    path('certifications/<int:pk>/delete', views.certification_delete, name='cv_certification_delete'),
    path('education', views.educations, name='cv_education'),
    path('educations/create', views.education_create, name='cv_education_create'),
    path('educations/<int:pk>/edit', views.education_edit, name='cv_education_edit'),
    path('educations/<int:pk>/delete', views.education_delete, name='cv_education_delete'),
    path('jobs', views.jobs, name='cv_jobs'),
    path('jobs/create', views.job_create, name='cv_job_create'),
    path('jobs/<int:pk>/edit', views.job_edit, name='cv_job_edit'),
    path('jobs/<int:pk>/delete', views.job_delete, name='cv_job_delete'),
]