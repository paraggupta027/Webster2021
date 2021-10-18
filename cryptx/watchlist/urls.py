from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.watchlist,name='watchlist'),
    path('create_watchlist/',views.create_watchlist,name='create_watchlist'),
]