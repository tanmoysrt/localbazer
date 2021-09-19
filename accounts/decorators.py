from django.shortcuts import redirect
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse
from functools import wraps
def buyer_required(view_func):
    @wraps(view_func)
    def wrap(request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.userflag==True:
                logout(request)
                return redirect('/account/buyerlogin/')
            else:
                return view_func(request,*args,**kwargs)
        else:
            return view_func(request,*args,**kwargs)
    return wrap

def seller_required(view_func):
    @wraps(view_func)
    def wrap(request,*args,**kwargs):
        if request.user.is_authenticated:
            if request.user.userflag==False:
                logout(request)
                return redirect('/account/sellerlogin/')
            else:
                return view_func(request,*args,**kwargs)
        else:
            return view_func(request,*args,**kwargs)
    return wrap