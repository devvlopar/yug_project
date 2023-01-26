from django.shortcuts import render, redirect
from django.conf import settings
import random
from django.core.mail import send_mail
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    try:
        seller_data = Seller.objects.get(email= request.session['seller_email'])
        return render(request, 'view_orders.html', {'seller_data': seller_data})
    except:
        return render(request, 'seller_login.html')

def add_product(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    return render(request, 'add_product.html', {'seller_data': seller_data})

def edit_product(request, pk):
    pro_obj = Product.objects.get(id = pk)
    if request.method == 'GET':
        seller_data = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'seller_data': seller_data, 'product_data': pro_obj})
    else:
        pro_obj.product_name = request.POST['product_name']
        pro_obj.des = request.POST['des']
        pro_obj.price = request.POST['price']
        pro_obj.pic = request.FILES['pic']
        pro_obj.save()
        seller_data = Seller.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'seller_data': seller_data, 'product_data': pro_obj})




def my_products(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    session_seller_pro = Product.objects.filter(seller = seller_data)
    return render(request, 'my_products.html', {'seller_data': seller_data, 'user_products': session_seller_pro})

def edit_profile(request):
    seller_data = Seller.objects.get(email = request.session['seller_email'])
    return render(request, 'seller_edit_profile.html', {'seller_data': seller_data})

def seller_register(request):
    if request.method == 'GET':
        return render(request, 'seller_register.html')
    else:
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request, 'seller_register.html', {'message': "Email Already Exists!!!"})

        except ObjectDoesNotExist:

            if request.POST['password'] == request.POST['repassword']:
                global seller_dict
                seller_dict = {
                    'full_name' : request.POST['full_name'],
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
                return render(request, 'seller_register.html', {'msg': 'Both Passwords are not Same!!!'})

def otp(request):
    if int(request.POST['u_otp']) == int(c_otp):
        c_otp = c_otp
        Seller.objects.create(
            full_name = seller_dict['full_name'],
            email = seller_dict['email'],
            password = seller_dict['password']
        )
        return render(request, 'seller_login.html', {'msg': "Account Created Successfully!!"})

    else:
        return render(request, 'otp.html', {'msg': 'OTP is wrong Enter again'})


def seller_login(request):
    if request.method == 'POST':
        try:
            user_obj = Seller.objects.get(email = request.POST['email'])
            if user_obj.password == request.POST['password']:
                request.session['seller_email'] = user_obj.email
                return render(request, 'view_orders.html', {'seller_data': user_obj})
            else:
                return render(request, 'seller_login.html', {'msg': "Password is Wrong!!!"})

        except:
            return render(request, 'seller_login.html', {'msg': 'Email Does Not Exist!!'})        
    else:
        try:
            request.session['seller_email']
            return redirect('index')
        except:
            return render(request, 'seller_login.html')


def seller_logout(request):
    try:
        del request.session['seller_email']
        return render(request, 'seller_login.html')
    except:
        return render(request, 'seller_login.html')

