from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

def dashboard(request):
    user = request.user
    if user.is_authenticated:
        name = user.first_name
        params = {
            'name' : name,
        }
        return render(request, 'dashboard/dash.html', params)

    return redirect('home')

def profile(request):
    user = request.user
    if user.is_authenticated:
        name = user.first_name
        lname = user.last_name
        email = user.username
        params = {
            'name' : name,
            'lname' : lname,
            'email' : email
        }
        return render(request , 'dashboard/profile.html',params)
    return redirect('home')

def resetpassword(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('password',"")
            confirm_password = request.POST.get('confirmpassword',"")

            if(password != confirm_password):
                return redirect('dashboard')

            user.set_password(password)
            print(password)
            user.save()
            user=authenticate(username=user.email,password=password)
            login(request,user)
            return redirect('dashboard')

    return redirect('home')


