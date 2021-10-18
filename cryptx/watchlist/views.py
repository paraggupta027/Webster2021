from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4
from django.core import serializers
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


def see_watchlist(request,watchlist):
    user=request.user
    if user.is_authenticated:
        watchlist_qs = WatchList.objects.get(user=user,name=watchlist)
        coins = watchlist_qs.coins.all()
        coins = coins.order_by('name')
        print(coins)
        if not watchlist_qs:
            return HttpResponse("No such watchlist")
        context = {
            'coins':coins,
            'name':watchlist
        }
        return render(request,'watchlist/see_watchlist.html',context)

    return redirect('home')


