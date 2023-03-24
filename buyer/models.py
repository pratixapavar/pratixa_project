from django.db import models

# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.TextField(max_length=300)
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=10,null=True, blank=True)
    
    
    def __str__(self):
        return self.email
    

class Cart(models.Model):
    product_name =models.CharField(max_length=50)
    price = models.FloatField(default=10.0)
    pic = models.FileField(upload_to= 'cart_products', default='sad.jpg')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self):
        return self.buyer.first_name