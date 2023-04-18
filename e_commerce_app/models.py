from django.db import models
from datetime import date
from django.utils import timezone


# Create your models here.
#Define a django enumeration
class ClientType(models.TextChoices):
    normal=('NORMAL','Normal Customer')
    loyal=('LOYAL','Loyal Customer')
    vip=('VIP','VIP Customer')
class Address(models.Model):
    houseNumber = models.PositiveSmallIntegerField(default=0)
    street = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    postalCode = models.CharField(max_length=50, default='')

    class Meta:
        db_table = 'address'
        ordering = ['country', 'city']
    def __str__(self):
        return f'id = {self.id}'
    


class User(models.Model):
    name = models.CharField(max_length=50, default='')
    password = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['email']

    def __str__(self):
        return f'name={self.name}, email={self.email}, phone={self.phone}'


class Provider(User):
    site_url = models.URLField(default='')

    class Meta:
        db_table = 'providers'
        

    def __str__(self):
        # return f'name={self.name}, email={self.email}, phone={self.phone}, site_url={self.site_url}'
        # or
        #return super().__str__() + f', site_url={self.site_url}'
        return self.name


class Product(models.Model):
    # id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=100, default='')
    price = models.FloatField(default=0)
    stock = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField(upload_to='images/product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    expirationDate = models.DateField(default=date(2023, 12, 31))
    fabricationDate = models.DateField(default=timezone.now)
    # on_delete have many options: CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET(), DO_NOTHING
    # CASCADE: when the referenced object is deleted, also delete the objects that have references to it
    # PROTECT: when the referenced object is deleted, raise a ProtectedError without deleting the object
    # SET_NULL: when the referenced object is deleted, set the forign key column to null
    # SET_DEFAULT: when the referenced object is deleted, set the forign key column to the default value
    # SET(): when the referenced object is deleted, set the forign key column to the value passed as parameter
    # DO_NOTHING: when the referenced object is deleted, do nothing
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'products'
        # tuples in products table are ordered by label in ascending
        # and then by price in descending order
        ordering = ['label', '-price']

    def __str__(self):
        # return 'label = ',self.label,', price = ',self.price,', stock = ',self.stock
        # return 'label = {}, price = {}, stock = {}'.format(self.label,self.price,self.stock)
        # return 'label=%s, price=%s, stock=%s'%(self.label,self.price,self.stock)
        #return f'label={self.label}, price={self.price}, stock={self.stock},'
        return f'id={self.id}'

class Client(User):
    familyName = models.CharField(max_length=100, default='')
    #typeClient = models.CharField(max_length=50, choices=[('LOYAL', 'Loyal Customer'), ('NORMAL', 'Normal Customer'),('VIP', 'Very Import Customer')], default='NORMAL')
    typeClient = models.CharField(max_length=50, choices=ClientType.choices, default=ClientType.normal)
    client_products = models.ManyToManyField(Product, through='Command', through_fields=('client', 'product'))

    class Meta:
        db_table = 'clients'
    def __str__(self):
        return f'id={self.id}'
    

class Command(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_cmd = models.DateField(default=timezone.now)
    quantity = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        # the table name in database is commands
        db_table = 'commands'
        # tuples in commands table are ordered by date_cmd in descending order
        ordering = ['-date_cmd']
        # the name of the table in admin panel is Command table (a name readable by humans)
        verbose_name = 'Command table'
        # the name of plural objects in admin panel is Commands List (a name readable by humans)
        verbose_name_plural = 'Command List'
        # the combination of client, product and date_cmd must be unique
        unique_together = [('client', 'product', 'date_cmd')]
