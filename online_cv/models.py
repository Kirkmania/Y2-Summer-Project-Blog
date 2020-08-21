from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.
class CV(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text=RichTextField(blank=True, null=True)
    
    def __str__(self):
        return self.text

class cvPersonalDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=200)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class cvProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text=RichTextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class cvEducation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '%s %s' % (self.user.get_full_name(), self.subject)

class cvWorkHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return '%s %s' % (self.user.get_full_name(), self.job_title)