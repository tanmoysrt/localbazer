from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'accounts'
urlpatterns = [
    path('buyerregister/',views.BuyerRegister,name='buyerregistration'),
    path('sellerregister/',views.SellerRegister,name='sellerregistration'),
    path('buyerlogin/',views.BuyerLogin,name='buyerlogin'),
    path('sellerlogin/',views.SellerLogin,name='sellerlogin'),
    path('sellerlogout/',views.sellerlogout,name='sellerlogout'),
    path('buyerlogout/',views.buyerlogout,name='buyerlogout'),
    path('verify/<int:phoneno>',views.verifyotp),
    path('resend/',views.resendotp),
    path('forget/',views.forgetpass)
]
