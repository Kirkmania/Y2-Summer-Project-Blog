from django.contrib import admin
from .models import Post, Comment    #import our post model we made
from django.contrib.auth.models import Permission

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')

# Register your models here.
admin.site.register(Post)   #register our post model
admin.site.register(Comment)