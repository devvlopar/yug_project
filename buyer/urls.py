from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('privacy/', privacy, name='home'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp')
    
]

#models, database tables

# SQL : structured query language
# ORM : Object Relational Mapping

#html : structure
#css : styles/ looks
#JS : animation,responsiveness