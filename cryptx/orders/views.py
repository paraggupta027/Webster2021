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



def handle_buy(request):
    user=request.user
    if user.is_authenticated and request.method=='POST':
        coin_symbol = request.POST.get("symbol")
        quantity = float(request.POST.get("quantity"))

        is_executable=Order.can_be_executed(user,coin_symbol,quantity,"BUY")
        
        msg =""
        if is_executable ==True:
            msg="Order was executed Successfully"
        else:
            msg=is_executable[1]
        resp={
            'msg':msg,
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type='application/json')

    return redirect('home')
def handle_sell(request):
    user = request.user
    if user.is_authenticated and request.method=='POST':
        coin_symbol = request.POST.get("symbol")
        quantity = float(request.POST.get("quantity"))

        is_executable=Order.can_be_executed(user,coin_symbol,quantity,"SELL")
        
        msg =""
        if is_executable ==True:
            msg="Order was executed Successfully"
        else:
            msg=is_executable[1]
        resp={
            'msg':msg,
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type='application/json')