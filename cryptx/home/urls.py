from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signuph/',views.signuphandle,name='signuph'),
    path('logout/',views.logout_user,name='logout'),
    path('login/',views.login_page,name='login_page'),
    path('forgotpassword/',views.forgotpassword , name = 'forgotpassword'),
    path('handleforgotpassword', views.handle_forgotpassword , name = 'handle_forgot_password')
]