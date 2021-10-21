from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.watchlist,name='watchlist'),
    path('add_coin',views.add_coin, name = 'add_coin'),
    path('create_watchlist/',views.create_watchlist,name='create_watchlist'),
    path('<str:watchlist>/',views.see_watchlist,name='see_watchlist')
]