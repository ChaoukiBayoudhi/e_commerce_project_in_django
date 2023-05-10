
from django.shortcuts import render
from .models import Address, Product,Client, Provider,Command
from rest_framework import viewsets,authentication,permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Max,Min
#import timezone
from django.utils import timezone
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
        #detail=True if the method is applied to a specific object
        #detail=False if the method is applied to a list of objects (all objects)
        @action(methods=['get'],detail=False)
        def max_min_price(self,request):
            if request.method!='GET':
                return Response({'message':'The method is not allowed','status':status.HTTP_405_METHOD_NOT_ALLOWED})
            #get the maximum price
            max_price = Product.objects.aggregate(Max('price'))['price__max']
            #get the minimum price
            min_price = Product.objects.aggregate(Min('price'))['price__min']
            #get the product with the maximum price
            p_max=Product.objects.get(price=max_price)
            #get the product with the minimum price
            p_min=Product.objects.get(price=min_price)
            #serialize p_max and p_min
            serializer = ProductSerializer(p_max)
            #if the object is a list of objects, we should use many=True
            #serializer = ProductSerializer(p_max,many=True)
            serializer1 = ProductSerializer(p_min)
            return Response({'Product with max price':serializer.data,'Product with price':serializer1.data})
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

    #define a custom method to get the products in stock ordered by a given client
    #The method should return products ordered by a given client in a period
    @action(detail=True, methods=['get'])
    #1st case
    #the method signature should as the line below, if the url is
    #http://localhost:8000/command/1/client_products?start_date=2020-01-01&end_date=2020-12-31
    #def client_products(self, request, pk=None):
    #2nd case
    #if the url is http://localhost:8000/command/client_products?client_id=1&start_date=2020-01-01&end_date=2020-12-31
    #the method signature should be as the line below
    def client_products(self, request):
        #the line below is for the 2nd case
        #get the client_id, start_date and end_date from the url
        #client_id, start_date and end_date are the query parameters name
        client_id = request.query_params.get('client_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        #if request parameters are not null (the client has initiated the request parameters)
        if client_id and start_date and end_date:
            try:
                client = Client.objects.get(pk=client_id)
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            except (ValueError, Client.DoesNotExist):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            #get the commands of the client between the start_date and the end_date
            commands = Command.objects.filter(client=client, date_cmd__range=[start_date, end_date])
           #create a list of product ids
            product_ids = [command.product.id for command in commands]
            #get the products of the client between the start_date and the end_date that are in stock
            products = Product.objects.filter(id__in=product_ids, stock__gt=0).order_by('label')
            #serialize the products => convert the products objects to json
            serializer = ProductSerializer(products, many=True)
            #serializer.data return a json array (or list)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    #get clients that are not satisfied
    #clients have ordered products but the ordered quantity  is insufficient
    #focus on command passed in given period
    #in the browser or in a front-end the url will be like
    #we have two query parameters start_date and end_date
    @action(detail=False, methods=['get'])
    #request is the http entity sent by the front-end or the client to the backend
    #request contains the headers and the body(data)
    #the headers contain the request method (GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD), encoding, content-type, authorization, etc...
    def not_satisfied_clients(self, request):
        #get the start_date and end_date from the url
        #the None is the default value if the query parameter is not provided
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        #if request parameters are not null (the client has initiated the request parameters)
        if start_date and end_date:
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            #get the commands between the start_date and the end_date
            commands = Command.objects.filter(date_cmd__range=[start_date, end_date])
            #create a list of client ids
            client_ids = [command.client.id for command in commands]
            #get the clients that have ordered products but the ordered quantity  is insufficient
            clients = Client.objects.filter(id__in=client_ids, client_products__stock__lte=0).distinct().order_by('name')
            #serialize the clients => convert the clients objects to json
            #many=True because we have a list of clients
            serializer = ClientSerializer(clients, many=True)
            #serializer.data return a json array (or list)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)