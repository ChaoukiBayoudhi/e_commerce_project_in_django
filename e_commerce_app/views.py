from django.shortcuts import render
from .models import Product,Client
from rest_framework import viewsets
from .serializers import ProductSerializer,ClientSerializer
# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    class Meta:
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        
class ClientViewSet(viewsets.ModelViewSet):
    class Meta:
        queryset = Client.objects.all()
        serializer_class = ClientSerializer
        #the following line is to allow the http methods get,post,put,delete
        #it is not necessary because the default value is ['get','post','put','delete']
        http_method_names=['get','post']