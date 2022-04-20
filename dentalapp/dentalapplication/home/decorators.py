from django.http import Http404
from django.shortcuts import redirect



def login_required(view_func):
    
    def wrapper_func(request, *args, **kwargs):
        print("--------", request.user.first_name)

        if request.user.username:
            return view_func(request, *args, **kwargs)
    
        else:
            raise Http404
        
    return wrapper_func
        