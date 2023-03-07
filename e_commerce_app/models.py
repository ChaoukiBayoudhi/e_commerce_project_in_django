from django.db import models
from datetime import date
# Create your models here.
class Product(models.Model):
    #id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=100,default='')
    price = models.FloatField(default=0)
    stock=models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='images/product_images',null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    expirationDate=models.DateField(default=date(2023,12,31))
    fabricationDate=models.DateField(default=date.today())

class Client(models.Model):
    name=models.CharField(max_length=100,default='')
    familyName=models.CharField(max_length=100,default='')
    email=models.EmailField(null=True,blank=True)
    phone=models.CharField(max_length=20,default='+21622000000')
    typeClient=models.CharField(max_length=50,choices=[('LOYAL','Loyal Customer'),('NORMAL','Normal Customer'),('VIP','Very Import Customer')],default='NORMAL')
