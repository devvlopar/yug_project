from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('', home, name='home'),
    path('yug/', yug, name="yug"),
    path('add_row/', add_row, name="add_row"),
    path('del/',del_row, name="del_row")
]

#models, database tables

# SQL : structured query language
# ORM : Object Relational Mapping

#html : structure
#css : styles/ looks
#JS : animation,responsiveness