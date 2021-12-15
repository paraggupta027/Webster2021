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
from orders.models import Order

def coin_chart_page(request,coin_name):
    user=request.user
    if user.is_authenticated:

        coin=Coin.objects.get(name=coin_name)

        context = {
            'coin':coin

        }

        return render(request,'charts/coin_chart.html',context)
    return redirect('home')

