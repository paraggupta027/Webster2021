from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.learn , name = 'learn'),
    path('crypto_basics/' , views.crypto_basics , name = 'crypto_basics'),
]