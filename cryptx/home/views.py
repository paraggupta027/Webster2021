from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4


def home(request):
    return render(request,'home/index.html')


def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')
    return render(request,'home/signup.html')



def signuphandle(request):

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        fname = request.POST.get('fname',"")
        lname = request.POST.get('lname',"")
        email = request.POST.get('email',"")
        password = request.POST.get('password',"")
        cpassword = request.POST.get('cpassword',"")

        if password != cpassword:
            print("Password did not match")
            return redirect('home')

        all_users = User.objects.all()

        for user in all_users:
            if user.email == email:
                print("Email already taken")
                return redirect('home')

        new_user = User.objects.create_user(username=email,password=password)
        new_user.email=email
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.save()

        user = authenticate(username=email,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
    
    return redirect('home')



def login_page(request):
    user=request.user
    if user.is_authenticated:
        return redirect('dashboard')
    
    if request.method=='POST':
        email = request.POST.get('email',"")
        password = request.POST.get('password',"")

        cur_user = User.objects.filter(username=email)
        if  len(cur_user)==0:
            print("No such user")
            return redirect('signup')

        user = authenticate(username=email,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')

    return render(request,'home/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')
