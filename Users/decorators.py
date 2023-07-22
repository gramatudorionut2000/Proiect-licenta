from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('DMS-home')
        else: 
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def unauthorised_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_manager is False:
            return redirect('unauthorised')
        else: 
            return view_func(request, *args, **kwargs)
    
    return wrapper_func