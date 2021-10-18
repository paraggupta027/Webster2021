from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json

from coins.models import Coin
from watchlist.models import WatchList


def watchlist(request):
    user=request.user
    if user.is_authenticated:
        watchlist_qs = WatchList.objects.filter(user=user)
        context={
            'watchlists':watchlist_qs
        }
        return render(request , 'watchlist/watchlist.html', context)

    return redirect('home')


def create_watchlist(request):
    user=request.user
    if user.is_authenticated and request.method=='POST':
        watchlist = request.POST.get('watchlist')

        new_watchlist = WatchList.objects.create(name=watchlist,user=user)
        new_watchlist.save()

        return redirect('watchlist') 
    return redirect('home')




