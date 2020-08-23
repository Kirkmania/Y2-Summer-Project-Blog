from django.contrib import admin
from .models import *  #import our post model we made

# Register your models here.
admin.site.register(CV)
admin.site.register(cvPersonalDetails)
admin.site.register(cvProfile)
admin.site.register(cvEducation)
admin.site.register(cvWorkHistory)
admin.site.register(cvExtras)