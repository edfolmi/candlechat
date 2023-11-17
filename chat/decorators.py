from django.http import HttpResponse
from django.shortcuts import redirect


def only_unauthenticated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return func(request, *args, **kwargs)
    return wrapper_func
