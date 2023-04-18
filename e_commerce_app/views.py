from django.shortcuts import render
from .models import Address, Product,Client, Provider,Command
from rest_framework import viewsets,authentication,permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Max,Min
from .serializers import AddressSerializer, CommandSerializer, ProductSerializer,ClientSerializer, ProviderSerializer
# Overview of Django predefined methods: all(), save(), create(), filter(),exclude(), aggregate(),values()
#select * from product; => res=Product.objects.all()
#select * from product where id=1; => res=Product.objects.get(id=1) or res=Product.objects.filter(id=1) or res=Product.objects.get(pk=1)
#select label,price from product; => res=Product.objects.values('label','price')
#select label,price from product where id=1; => res=Product.objects.values('label','price').get(id=1) or res=Product.objects.values('label','price').filter(id=1)
#insert into product(label,price) values('product1',100); => res=Product(label='product1',price=100).save() or p=Product(label='product1',price=100) Product.objects.create(p)
#update product set label='product1',price=100 where id=1; => res=Product.objects.get(id=1).update(label='product1',price=100) or p=Product.objects.get(id=1) p.label='product1' p.price=100 p.save()
#delete from product where id=1; => res=Product.objects.get(id=1).delete() or p=Product.objects.get(id=1) p.delete()
#Examples of custom requests using exclude(),filter(),aggregate(),values(), count(),distinct(),order_by(),reverse(),first(),last(),exists(),in_bulk(),get_or_create(),update_or_create(),bulk_create(),bulk_update()
#select the maximum and the minimum price => res=Product.objects.aggregate(Max('price'),Min('price'))
#select expirationDate before 2023-12-01 => res=Product.objects.distinct().filter(expirationDate__lt='2023-12-01').order_by() 
class ProductViewSet(viewsets.ModelViewSet):
    
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        #add  some custom methods to the viewset
        @action(methods=['get'],detail=True)
        def max_min_price(self,request):
            if request.method!='GET':
                return Response({'message':'the method is not allowed','status':status.HTTP_405_METHOD_NOT_ALLOWED})
            #get the maximum and the minimum price
            res=Product.objects.aggregate(Max('price'),Min('price'))
            return Response({'max price ':res(0),'min price':res(1)})
class ClientViewSet(viewsets.ModelViewSet):
    
        queryset = Client.objects.all()
        serializer_class = ClientSerializer
        #the following line is to allow the http methods get,post,put,delete
        #it is not necessary because the default value is ['get','post','put','delete']
        #http_method_names=['get','post']
        #the following line is to allow the authentication
        #it is not necessary because the default value is TokenAuthentication
        #other values are SessionAuthentication,BasicAuthentication
        #the default value is TokenAuthentication
        #SessionAuthentication is to use the session of the browser
        #BasicAuthentication is to use the username and password
        #===>authentication_classes=[authentication.TokenAuthentication]
        #the following line is to allow the permission
        #it is not necessary because the default value is IsAuthenticated
        #other values are IsAdminUser,IsAuthenticatedOrReadOnly,AllowAny
        #IsAdminUser is to allow the admin user to use the methods get,post,put,delete
        #IsAuthenticatedOrReadOnly is to allow the authenticated user to use the methods get,post,put,delete
        # and the not authenticated user to use the method get
        #AllowAny is to allow any user to use the methods get,post,put,delete
        #the default value is IsAuthenticated
        #==>permission_classes=[permissions.IsAuthenticated]












       #define a custom method to get the products of a client
        @action(methods=['get'],detail=True)
        def get_products(self,request,pk=None):
            #get the client
            client = Client.objects.get(id=pk)
            #get the products of the client
            products = client.products.all()
            #serialize the products
            serializer = ProductSerializer(products,many=True)
            #return the products
            return Response(serializer.data)
        #define a custom method to add a product to a client
        @action(methods=['post'],detail=True)
        #details=True because we are going to use the primary key of the client.
        #we would to perform the action on a single instance of client
        def command_product(self,request,pk=None):
            #get the client
            client = Client.objects.get(id=pk)
            #get the product
            product = Product.objects.get(id=request.data['product_id'])
            
            #add the product to the client
            client.client_products.add(product)
            #save the client
            client.save()
            #return the client
            return Response({'message':f'Command of product {product.label} by the client {client.name} was accepted'})
        #define a custom method to remove a product from a client
        @action(methods=['delete'],detail=True)
        def remove_product(self,request,pk=None):
            #get the client
            client = Client.objects.get(id=pk)
            #get the product
            product = Product.objects.get(id=request.data['product_id'])
            #remove the product from the client
            client.products.remove(product)
            #save the client
            client.save()
            #return the client
            return Response({'message':'Product removed from the client'})
        #define a custom method to perform more than one action
        @action(methods=['get','post'],detail=True)
        def products(self,request,pk=None):
            if request.method == 'GET':
                return self.get_products(request,pk)
            elif request.method == 'POST':
                return self.add_product(request,pk)

        #define a custom method to perform more than one action
        @action(methods=['get','post','delete'],detail=True)
        def products2(self,request,pk=None):
            if request.method == 'GET':
                return self.get_products(request,pk)
            elif request.method == 'POST':
                return self.add_product(request,pk)
            elif request.method == 'DELETE':
                return self.remove_product(request,pk)

#define the Address CRUD using the ModelViewSet
class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer

#define the Provider CRUD using the ModelViewSet
class ProviderViewSet(viewsets.ModelViewSet):
    queryset=Provider.objects.all()
    serializer_class=ProviderSerializer

#define the Command CRUD using the ModelViewSet
class CommandViewSet(viewsets.ModelViewSet):
    queryset=Command.objects.all()
    serializer_class=CommandSerializer