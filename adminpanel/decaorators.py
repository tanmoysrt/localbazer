from django.contrib.auth import logout
from django.shortcuts import redirect
from functools import wraps


def toplevel_superuser_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser and request.user.is_active:
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect('/admin/login/')
        else:
            return view_func(request, *args, **kwargs)

    return wrap
