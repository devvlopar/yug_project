from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def index(request):
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
    return render(request, 'register.html')