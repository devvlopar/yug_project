from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import random
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def index(request):
    try:
        s_email = request.session['email']
        user_obj = Buyer.objects.get(email = s_email)
        return render(request, 'index.html', {'user_data' : user_obj})
    except:
        return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def faqs(request):
    return render(request, 'faqs.html')

def privacy(request):
    return render(request, 'privacy.html')

def yug(request):
    return HttpResponse("this is yug's message")

def add_row(request):
    Buyer.objects.create(
        first_name = 'kiran',
        last_name = 'patel',
        email = 'devang@gmail.com',
        password = 'Tops123',
        address = 'A-301, Society,road,surat',
        mobile = '9089786756'
    )
    return HttpResponse('Row Created!!')

def del_row(request):
    r1 = Buyer.objects.get(email = 'khushal@gmail.com') #single row, object
    r1.delete()

    return HttpResponse('Deleted!!!')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            Buyer.objects.get(email = request.POST['email'])
            return render(request, 'register.html', {'message': "Email Already Exists!!!"})

        except ObjectDoesNotExist:

            if request.POST['password'] == request.POST['repassword']:
                global user_dict
                user_dict = {
                    'first_name' : request.POST['first_name'],
                    'last_name' : request.POST['last_name'],
                    'email' : request.POST['email'],
                    'password' : request.POST['password']
                }
                global c_otp
                c_otp = random.randint(100_000, 999_999)
                subject = 'Sign Up For Ecommerce!!'
                message = f'Hello User,\nYour OTP is {c_otp}.'
                f_email = settings.EMAIL_HOST_USER
                r_list = [request.POST['email']]
                send_mail(subject, message, f_email, r_list)
                return render(request, 'otp.html', {'msg': 'Check Your MailBox!!'})

            else:
                return render(request, 'register.html', {'msg': 'Both Passwords are not Same!!!'})

def otp(request):
    if int(request.POST['u_otp']) == int(c_otp):
        c_otp = c_otp
        Buyer.objects.create(
            first_name = user_dict['first_name'],
            last_name = user_dict['last_name'],
            email = user_dict['email'],
            password = user_dict['password']
        )
        return HttpResponse('Ho gya')
    else:
        return render(request, 'otp.html', {'msg': 'OTP is wrong Enter again'})


def login(request):
    if request.method == 'POST':
        try:
            user_obj = Buyer.objects.get(email = request.POST['email'])
            if user_obj.password == request.POST['password']:
                request.session['email'] = user_obj.email
                return render(request, 'index.html', {'user_data': user_obj})
            else:
                return render(request, 'login.html', {'msg': "Password is Wrong!!!"})

        except:
            return render(request, 'login.html', {'msg': 'Email Does Not Exist!!'})        
    else:
        try:
            request.session['email']
            return redirect('index')
        except:
            return render(request, 'login.html')


def logout(request):
    del request.session['email']
    return redirect('index')




# 1. pass& reenter
# 2. email already
# 
# 
# OTP procees