from django.db import models

# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=70)
    address = models.TextField(max_length=500)
    mobile = models.CharField(max_length=15)




    
