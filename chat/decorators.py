from django.http import HttpResponse


def only_authenticated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('user must login!')
    return wrapper_func
