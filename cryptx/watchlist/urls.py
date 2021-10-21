from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.watchlist,name='watchlist'),
    path('create_watchlist/',views.create_watchlist,name='create_watchlist'),
    path('add_coin/',views.add_coin,name='add_coin'),
    path('delete_coin/',views.delete_coin,name='delete_coin'),
    path('<str:watchlist>/',views.see_watchlist,name='see_watchlist'),
]