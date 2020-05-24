from django.contrib import admin
from .models import Post, Comment    #import our post model we made

# Register your models here.
admin.site.register(Post)   #register our post model
admin.site.register(Comment)