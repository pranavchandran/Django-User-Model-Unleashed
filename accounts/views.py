from django.http import HttpResponseRedirect,Http404
from django.contrib.auth import (
                                login,
                                get_user_model,
                                logout
                                )
from django.shortcuts import render
from .forms import UserCreationForm,UserLoginForm
from .models import ActivationProfile

User = get_user_model()

def register(request,*args,**kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/login")

    return render(request,"accounts/register.html",{"form":form})

def user_login(request,*args,**kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get("user_obj")
        # user_obj = User.objects.get(username__iexact=query)
        login(request,user_obj)
        return HttpResponseRedirect("/")
    return render(request,"accounts/login.html",{"form":form})

def home(request):
    if request.user.is_authenticated:
        print(request.user.profile.user)
    return render(request,"accounts/home.html",{})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def activate_user_view(request,code=None,*args,**kwargs):
    if code:
        act_profile_qs = ActivationProfile.objects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count()==1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user_obj=act_obj.user
                user_obj.is_active = True
                user_obj.save()
                act_obj.expired=True
                act_obj.save()
                return HttpResponseRedirect('/login')
        # invalid code
        raise Http404




