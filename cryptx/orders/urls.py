from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('handle_buy/',views.handle_buy,name='handle_buy'),
    path('wallet/', views.wallet_view.as_view(), name='wallet'),
    path('charge/', views.charge, name='charge'),
    path('handle_sell/',views.handle_sell,name='handle_sell'),
    path('order_history/',views.order_history,name='order_history')
]