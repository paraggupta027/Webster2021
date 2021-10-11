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

def dashboard(request):
    user=request.user
    if user.is_authenticated:
        return render(request, 'dashboard/dash.html')
    return redirect('home')


def isCoinMatching(str1 , str2):
    #Filters user based on search
    m = len(str1) 
    n = len(str2) 
      
    j = 0   
    i = 0   
      
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
    return j==m 


def live_search(request,*args):
    user=request.user
    if user.is_authenticated:
        query = request.GET.get('query')
        all_coins = Coin.objects.all()

        search_qs = []
        for coin in all_coins:
            if isCoinMatching(coin.name,query) or isCoinMatching(query,coin.name):
                search_qs.append(coin.name)

        resp={
            'coins':search_qs,
        }
    response=json.dumps(resp)
    return HttpResponse(response,content_type='application/json')

    return redirect('home')