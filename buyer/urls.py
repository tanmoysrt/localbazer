from django.urls import path
from . import views

app_name='buyer'
urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search),
    path('product/',views.orderdetails),
    path('checkpin',views.checkpin),
    path('cart/',views.cart,name='cart'),
    path('orderhistory/',views.orderhistory),
    path('shopcategory/',views.shopcategory),
    path('shoppage',views.shoppage),
    path('profile',views.accountspage),
    path('refer/',views.referralpage),
]

