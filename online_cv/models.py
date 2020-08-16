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