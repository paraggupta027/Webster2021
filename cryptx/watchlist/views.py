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
from django.http import JsonResponse

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
        watchlist_qs = WatchList.objects.filter(name=watchlist,user=user)

        if not watchlist_qs:
            return HttpResponse("No such watchlist")

        watchlist_qs=watchlist_qs[0]
        coins = watchlist_qs.coins.all()
        all_coins = Coin.objects.all()

        coins_qs = []
        for coin in coins:
            coins_qs.append({'name':coin.name,'symbol':coin.symbol})

        context = {
            'all_coins':all_coins,
            'coins_qs':coins_qs,
            'name':watchlist
        }
        return render(request,'watchlist/see_watchlist.html',context)

    return redirect('home')


def add_coin(request,*args):
    user = request.user
    if user.is_authenticated:
        coin = request.GET['coin']
        name = request.GET['name']

        WatchList.addcoin(coin,name,user)
        return JsonResponse({})

    return redirect('home')


def delete_coin(request,*args):
    user = request.user
    if user.is_authenticated:
        coin = request.GET['coin']
        name = request.GET['name']

        WatchList.remove_coin(coin,name,user)
        return JsonResponse({})

    return redirect('home')

def delete_watchlist(request,*args):
    user = request.user
    if user.is_authenticated:

        name = request.GET['name']

        watchlist = WatchList.objects.get(name = name , user = user)
        print("hello")
        print(watchlist)
        watchlist.delete()

        return JsonResponse({})

    return redirect('home')
