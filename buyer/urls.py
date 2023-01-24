from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('privacy/', privacy, name='home'),
    path('register/', register, name='register'),
    path('otp/', otp, name='otp'),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('buyer_edit_profile/', buyer_edit_profile, name="buyer_edit_profile"),


    
]

#models, database tables

# SQL : structured query language
# ORM : Object Relational Mapping

#html : structure
#css : styles/ looks
#JS : animation,responsiveness