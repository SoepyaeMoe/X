from rest_framework.response import Response
from .models import Blog
from .helper import error_response

def login_required(fun):
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous:
            return Response(error_response('unauthorized'))
        return fun(request, *args, **kwargs)
    return wrapper

def owner_only(m):
    def decorator(fun):
        def wrapper(request, pk):
            try:
                x = m.objects.get(id=pk)
            except m.DoesNotExist:
                return Response(error_response('Unknown data'))
            if request.user != x.author:
                return Response(error_response('You don\'t have permission'))
            return fun(request, pk)
        return wrapper
    return decorator