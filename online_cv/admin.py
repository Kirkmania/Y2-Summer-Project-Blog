from django.contrib import admin
from .models import CV, cvPersonalDetails   #import our post model we made

# Register your models here.
admin.site.register(CV)
admin.site.register(cvPersonalDetails)