from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

# NOTE: My first django model! Pog!
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, config_name='blog')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=255, default='uncategorised')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    # Added in order to count number of approved comments in post list
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

######################
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post_list')

######################
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.title