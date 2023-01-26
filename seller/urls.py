from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('add_product/', add_product, name="add_product"),
    path('edit_product/<int:pk>', edit_product, name="edit_product"),
    path('my_products/', my_products, name="my_products"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('seller_login/', seller_login, name="seller_login"),
    path('seller_logout/', seller_logout, name="seller_logout"),
    path('seller_register/', seller_register, name="seller_register"),


]