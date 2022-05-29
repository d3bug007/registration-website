from django.shortcuts import render,redirect
from django.http import HttpResponse
from registration_app.forms import UserForm, UserProfileInfoForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def index(request):
    return render(request,'registration_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('registration_app:user_login')

def register(request):

    registered = False

    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:

            print(user_form.errors,profile_form.errors)
    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(request,'registration_app/user_registration.html',
                {'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered})

def user_login(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user:

            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            return HttpResponse("USERNAME OR PASSWORD NOT WORKING")

    else:
        return render(request,'registration_app/login.html',{})
