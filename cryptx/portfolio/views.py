from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4

import json

from coins.models import Coin
from portfolio.models import Portfolio
from orders.models import Order
from dashboard.models import Profile

from django.conf import settings
from django.views.generic.base import TemplateView
import stripe

# Create your views here.


def portfolio_home(request):
    user  = request.user
    if user.is_authenticated:
        portfolios = Portfolio.objects.filter(user=user)
        portfolio_qs = []
        for portfolio in portfolios:
            portfolio_qs.append({
                'name':portfolio.coin.name,
                'symbol':portfolio.coin.symbol,
                'avg_price':portfolio.avg_price,
                'quantity':portfolio.quantity
            }) 
        context = {
            'portfolio':portfolio_qs
        }    
        return render(request,'portfolio/portfolio.html',context)
    return redirect('home')