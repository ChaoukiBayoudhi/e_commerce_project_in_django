from django.urls import include, path
from rest_framework import routers
from .views import AddressViewSet, ClientViewSet, CommandViewSet,ProductViewSet, ProviderViewSet
from e_commerce_app.views import ProductViewSet,ClientViewSet
#get an instance of the router defined in rest_framework
router=routers.DefaultRouter()
#add product urls (get,post,put,delete) to the router
router.register(r'products',ProductViewSet,basename='product')
router.register(r'clients',ClientViewSet,basename='client')
#add address urls (get,post,put,delete) to the router
router.register(r'addresses',AddressViewSet,basename='address')
router.register(r'providers',ProviderViewSet,basename='provider')
router.register(r'commands',CommandViewSet,basename='command')
urlpatterns = [
    #path is used to define a new router
    #include is used to include the urls defined in the router
    #Urls defined in the router are:
    #http://localhost:8000/ecommerce/products/ => get all products (GET method)
    #http://localhost:8000/ecommerce/products/1/ => get the product with id=1 (GET method)
    #http://localhost:8000/ecommerce/products/ => post a new product (POST method)
    #http://localhost:8000/ecommerce/products/1/ => put the product with id=1 (PUT or PATCH method)
    #http://localhost:8000/ecommerce/products/1/ => delete the product with id=1 (DELETE method)
    #Same urls for clients
    path('',include(router.urls)),
    path('max_min_price/', ProductViewSet.as_view({'get': 'max_min_price'}), name='max_min_price'),
    path(r'<int:pk>/client_products/', 
         CommandViewSet.as_view({'get': 'client_products'}), 
         name='client_products'),
]
