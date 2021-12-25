from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4



def learn(request):
    return render(request , 'learn/learn.html')

def crypto_basics(request):
    return render(request , 'learn/step1.html')

def earn_crypto(request):
    return render(request , 'learn/step2.html')

def trade_crypto(request):
    return render(request , 'learn/step3.html')

def use_crypto(request):
    return render(request , 'learn/step4.html')

def build_crypto(request):
    return render(request , 'learn/step5.html')