from django.http import HttpResponse
from django.shortcuts import redirect

# Decorators learned and used from https://youtu.be/eBsc65jTKvw
# Check that user is unauthenticated (e.g. to stop them from logging in after already logged in)
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post_list')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

# Check that user belongs to role with permission to view page (allowed roles is sent by decorator call)
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():            #i.e. if a user belongs to a group/queryset of groups
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('not_allowed')
        return wrapper_func
    return decorator