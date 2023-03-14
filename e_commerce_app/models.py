from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=50,default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20,default='')
    class Meta:
        abstract=True
        oredering=['email']
    
class Provider(User):
    site_url=models.URLField(default='')
    class Meta:
        db_table='providers'
class Product(models.Model):
    #id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=100,default='')
    price = models.FloatField(default=0)
    stock=models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='images/product_images',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    expirationDate=models.DateField(default=date(2023,12,31))
    fabricationDate=models.DateField(default=timezone.now)
    provider=models.ForeignKey(Provider,on_delete=models.CASCADE)
    class Meta:
        db_table='products'
        #tuples in products table are ordered by label in ascending
        #and then by price in descending order
        ordering=['label','-price']
class Client(User):
    familyName=models.CharField(max_length=100,default='')
    typeClient=models.CharField(max_length=50,choices=[('LOYAL','Loyal Customer'),('NORMAL','Normal Customer'),('VIP','Very Import Customer')],default='NORMAL')
    client_products=models.ManyToManyField(Product,through='Command',through_fields=('client','product'))
    class Meta:
        db_table='clients'
class Command(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_cmd=models.DateField(default=timezone.now)
    quantity=models.PositiveSmallIntegerField(default=1)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    class Meta:
        db_table='commands'
        ordering=['-date_cmd']


