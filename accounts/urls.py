from django.urls import path
from . import views
from .views import UserRegisterView

urlpatterns = [
    path('register/', views.signup, name='register'),
]