from rest_framework import serializers
from .models import Product,Client,Address,Provider,Command
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
class ProviderSerializer(serializers.ModelSerializer):
    #address=AddressSerializer(read_only=True)
    class Meta:
        model = Provider
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    #serialize the provider of the product (result of the foreign key relationship)
    #provider=ProviderSerializer()#read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
class ClientSerializer(serializers.ModelSerializer):
    address=AddressSerializer(read_only=True)
    #serialize the products of the client (result of the many to many relationship)
    #client_products=serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields='__all__'
        #fields = ('name','email','phone','typeClient')

class CommandSerializer(serializers.ModelSerializer):
    #product=ProductSerializer(read_only=True)
    #client=ClientSerializer(read_only=True)
    
    class Meta:
        model = Command
        fields = '__all__'