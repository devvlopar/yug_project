from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import random
from django.core.mail import send_mail
from django.conf import settings
from seller.models import *

import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def index(request):
    all_products = Product.objects.all()
    try:
        s_email = request.session['email']
        user_obj = Buyer.objects.get(email = s_email)
        return render(request, 'index.html', {'user_data' : user_obj, 'all_products': all_products})
    except:
        return render(request, 'index.html',{'all_products' : all_products})

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
                return redirect('index')
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

def buyer_edit_profile(request):
    if request.method == 'GET':
        try:
            user_data = Buyer.objects.get(email = request.session['email'])
            return render(request, 'buyer_edit_profile.html', {'user_data': user_data})
        except:
            return render(request, 'login.html')
    else:
        user_row = Buyer.objects.get(email = request.session['email'])
        user_row.first_name = request.POST['first_name']
        user_row.last_name = request.POST['last_name']
        user_row.address = request.POST['address']
        user_row.mobile = request.POST['mobile']
        user_row.pic = request.FILES['pic']
        user_row.save()
        
        user_data = Buyer.objects.get(email = request.session['email'])
        return render(request, 'buyer_edit_profile.html', {'user_data': user_data})


def add_to_cart(request, pk):
    try:
        buyer_obj = Buyer.objects.get(email = request.session['email'])
        product_obj =  Product.objects.get(id = pk)
        Cart.objects.create(
            product = product_obj,
            buyer = buyer_obj
        )
        return redirect('index')
    except:
        return render(request, 'login.html')


def cart(request):
    s_email = (request.session).get('email')
    if not s_email:
        return render(request, 'login.html')
    user_data = Buyer.objects.get(email = s_email)
    cart_list = Cart.objects.filter(buyer = user_data)
    total_price = 0
    for i in cart_list:
        total_price += i.product.price
    total_price *= 100
    currency = 'INR'
    global amount
    amount = int(total_price) # Rs. 200
    
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['user_data'] = user_data
    context['cart_list'] = cart_list
    context['total_price'] = total_price
    context['rupee_total_price'] = total_price / 100

    return render(request, 'cart.html', context=context)











# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
                }
            global amount
            amount = amount
            try:
                razorpay_client.payment.capture(payment_id, amount)
                return render(request, 'paymentsuccess.html')
            except:
                return render(request, 'paymentfail.html')
           
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()




def delete_cart_row(request, pk):
    del_row = Cart.objects.get(id = pk)
    del_row.delete()
    return redirect('cart')



# 1. pass& reenter
# 2. email already
# 
# 
# OTP procees