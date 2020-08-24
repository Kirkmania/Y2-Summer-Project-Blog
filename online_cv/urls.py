from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [  
    path('', views.cv_builder, name='cv_builder'),
    path('personal_details', views.personal_details, name='cv_personal_details'),
    path('profile', views.profile, name='cv_profile'),
    path('education', views.education, name='cv_education'),
    path('work_history', views.work_history, name='cv_work_history'),
    path('extras', views.extras, name='cv_extras'),
    path('skills', views.skills, name='cv_skills'),
    path('interests', views.interests, name='cv_interests'),
    path('languages', views.languages, name='cv_languages'),
    path('certifications', views.certifications, name='cv_certifications'),
    path('preview', views.preview, name='cv_preview'),
]