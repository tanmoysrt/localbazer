from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('pending',views.pendingorder,name='pendingorder'),
    path('delivered',views.deliveredorder,name='delivered'),
    path('allorder',views.allorder,name='allordered'),
    path('addproduct',views.addproduct,name='addproduct'),
    path('updateproduct',views.updateproduct,name='updateproduct'),
    path('deleteproduct',views.deleteproduct,name='deleteproduct'),
    path('deleterecord',views.deleterecord),
    path('editrecord',views.editrecord),
    path('picupdate',views.picupdate),
    path('deliveryconfig',views.deliveryconfig),
    path('editseller',views.editseller,name='editseller'),
    path('editshop',views.editshop,name='editshop'),
    path('deletepincode',views.deletepincode),
    path('addpincode',views.addpincode),
    path('updatestatus',views.updatestatus),
    path('allindiadelivery',views.changeallindiastatus),
    path('od/<int:idd>',views.showorderdata)
]