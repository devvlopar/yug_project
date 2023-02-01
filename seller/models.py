from django.db import models





# Create your models here.

class Seller(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=30)
    gst_no = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self) -> str:
        return self.full_name


class Product(models.Model):
    product_name = models.CharField(max_length=150)
    des = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places= 2, default=500)
    pic = models.FileField(upload_to='products_images', default='sad.jpg')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class MyOrders(models.Model):

    all_status = [
        ('pending', 'pending'),
        ('dispatched', 'dispatched')
    ]

    buyer = models.ForeignKey(to='buyer.Buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(choices= all_status,max_length=50, default='pending')

    def __str__(self):
        return str(self.id)

