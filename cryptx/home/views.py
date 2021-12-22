from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User

#Auth and messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from uuid import uuid4
from .models import Forgotpassword

from io import BytesIO
from xhtml2pdf import pisa
from django.template import Template


from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# from weasyprint import HTML

from django.conf import settings 
from django.core.mail import send_mail,EmailMessage
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from django.http import JsonResponse

# Models
from dashboard.models import Profile
from dashboard.models import TransactionHistory


def report_generator(request):
    user = request.user
    if user.is_authenticated and user.email==settings.COMPANY_EMAIL:
        all_users = User.objects.all()
        for user in all_users:
            if user.email!=settings.COMPANY_EMAIL:
                report_email_sender(user.email)

        return JsonResponse({})

    return redirect('home')


def report_email_sender(email):

    transaction_history = TransactionHistory.objects.filter(email=email)

    context = {
        'transaction_history':transaction_history
    }

    html  = render_to_string('home/report.html',context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    filename = 'report.pdf'
    to_emails = [email]
    subject = "Crypt-X daily report"
    email = EmailMessage(subject, "daily report brooo check it out", from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach(filename, pdf, "application/pdf")
    email.send(fail_silently=False)
    print(f'Report sent to {email}')


def home(request):
    user = request.user
    if user.is_authenticated and user.email==settings.COMPANY_EMAIL:
        return redirect('company_main_server')
        
    if user.is_authenticated:
        return redirect('dashboard')
    return render(request,'home/index.html')


def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')
    return render(request,'home/signup.html')



def signuphandle(request):

    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        fname = request.POST.get('fname',"")
        lname = request.POST.get('lname',"")
        email = request.POST.get('email',"")
        password = request.POST.get('password',"")
        cpassword = request.POST.get('cpassword',"")

        if password != cpassword:
            print("Password did not match")
            return redirect('home')

        all_users = User.objects.all()

        for user in all_users:
            if user.email == email:
                print("Email already taken")
                return redirect('home')

        new_user = User.objects.create_user(username=email,email = email,password=password)
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.save()

        Profile(email=email).save()

        user = authenticate(username=email,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
    
    return redirect('home')



def login_page(request):
    user=request.user

    if user.is_authenticated and user.email==settings.COMPANY_EMAIL:
        return redirect('company_main_server')

    if user.is_authenticated:
        return redirect('dashboard')

    print("login")
    
    if request.method=='POST':
        print("Post request")
        email = request.POST.get('email',"")
        password = request.POST.get('password',"")

        cur_user = User.objects.filter(username=email)
        if  len(cur_user)==0:
            print("No such user")
            return redirect('signup')

        user = authenticate(username=email,password=password)
        if user:
            print("User exists")
            login(request,user)
            return redirect('dashboard')
        print("Post request completed")

    return render(request,'home/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def forgotpassword(request):
    return render(request , 'home/forgot.html')


# shobhit.20194139@gmail.com

def handle_forgotpassword(request):
    if request.method == 'POST':
        print("Working")
        email = request.POST.get('email')

        user = User.objects.filter(username = email)

        if len(user) == 0:
            print("No such user")
            return redirect('home')

        token = uuid4()

        content = f"http://127.0.0.1:8000/auth_forgot/{token}"
        print("this is my " + content)

        send_mail('Forgot_password',content,'techstartechtechstar@gmail.com',[email],fail_silently=False)
        print("Mail sent")
        new_forgot = Forgotpassword(email=email ,token=token)
        new_forgot.save()
        print("Token saved")
        return redirect('login_page')

    return redirect('home')

def auth_forgot_password(request,token):
    forgotPassword = Forgotpassword.objects.filter(token = token)

    if len(forgotPassword != 0):
        response = {
            'token' : token
        }

        return render(request , 'home/resetpassword.html' , response)
    return redirect('home')

def reset_password(request,token):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request>POST.get('confirmpassword')

        if(new_password == confirm_password):
            user = Forgotpassword.objects.filter(token=token)
            user.set_password(new_password)
            print("Password successfully changed")
            return redirect('home')

    return redirect('forgotpassword')        



