from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [  
    path('', views.cv_builder, name='cv_builder'),
    path('personal_details', views.personal_details, name='cv_personal_details'),
    path('profile', views.profile, name='cv_profile'),
    path('education', views.education, name='cv_education')
]