from django.db import models
from datamanagement.models import ProductData,AllIndiaPinCode
from datamanagement.variable import ELECTRONICS_CATEGORY,FOOD_CATEGORY,GARMENTS_CATEGORY,GROCERY_CATEGORY,HANDCRAFTS_CATEGORY,STATIONARY_CATEGORY
from accounts.models import CustomUser
from seller.models import SellerProfile
from django import template
import json

register = template.Library()

@register.filter
def loadcartproductdetails(data):
    x= json.loads(data)
    return x["cart"]

@register.filter
def productNameFromId(data):
    product=ProductData.objects.filter(id=int(data))[0]
    name=product.name
    return name

@register.filter
def customerphone(data):
    x=CustomUser.objects.filter(id=int(data))[0]
    return x.phoneno

@register.filter
def customername(data):
    x=CustomUser.objects.filter(id=int(data))[0]
    return x.name
@register.filter
def customeremail(data):
    x=CustomUser.objects.filter(id=int(data))[0]
    return x.email

@register.filter
def customeraddress(data,arg):
    x=CustomUser.objects.filter(id=int(data))[0]
    y=json.loads(x.buyer.address)
    for i in y["address"]:
        if  int(i["id"]) == int(arg):
            return i["address"]

@register.filter
def customerpincode(data,arg):
    x=CustomUser.objects.filter(id=int(data))[0]
    y=json.loads(x.buyer.address)
    for i in y["address"]:
        if  int(i["id"]) == int(arg):
            return i["pincode"]


@register.filter
def discountedprice(data,arg):
    x=data*(100-arg)/100
    return round(x,2)

@register.filter
def jsonload(data):
    x= json.loads(data)
    return x

@register.filter
def getofficename(data):
    a=""
    for i in AllIndiaPinCode.objects.filter(pincode=int(data)):
        a=a+" , "+i.officename
    return a

@register.filter
def generateSubcategoryOption(data):
    x = ""
    if data=='fashion':
        x=GARMENTS_CATEGORY
    elif data=='food':
        x=FOOD_CATEGORY
    elif data=='grocery':
        x=GROCERY_CATEGORY
    elif data=='electronics':
        x=ELECTRONICS_CATEGORY
    elif data=='handcrafts':
        x=HANDCRAFTS_CATEGORY
    elif data=='stationary':
        x=STATIONARY_CATEGORY
    elif data=='garments':
        x=GARMENTS_CATEGORY
    generated=""

    if x != "":

        for i in range(len(x)):
            a,b= x[i]
            generated=generated+f"<option value='{a}'>{b}</option>"
    return generated

@register.filter
def getshopnamebyproduct(data):
    x=SellerProfile.objects.get(id=int(data))
    return x.shopname

@register.filter
def getshopnamebyorder(data):
    x=SellerProfile.objects.get(user_id=int(data))
    return x.shopname
@register.filter
def deliveryyesorno(data):
    x=SellerProfile.objects.get(id=int(data))
    if x.homedelivery==True:
        return "<b style='color: rgb(8, 202, 8)'>Home Delivery Available</b>"
    elif x.homedelivery==False:
        return "<b style='color: red;'>Home Delivery Not Avilable</b>"
@register.filter
def deliveryyesornotext(data):
    x=SellerProfile.objects.get(id=int(data))
    if x.homedelivery==True:
        return "Home Delivery Available"
    elif x.homedelivery==False:
        return "Home Delivery Not Avilable"
@register.filter
def delivertag(data):
    x=SellerProfile.objects.get(id=int(data))
    if x.homedelivery==True:
        return     '''<div class="alert alert-success" role="alert">
       Home Delivery &amp; Self Pickup Available
     </div>'''
    elif x.homedelivery==False:
        return '''    <div class="alert alert-warning" role="alert">
       Only Self Pickup Available
     </div>'''

@register.filter
def getproductphotourl(data):
    x=ProductData.objects.get(id=data).photo
    return x

@register.filter
def getsellerprofileid(data):
    x=SellerProfile.objects.get(user_id=int(data))
    return x.id
@register.simple_tag
def setvar(val=None):
  return val

@register.filter
def gettotalpriceofcart(data):
    y=json.loads(data)
    cart=y['cart']
    # print(cart)
    price=0
    for i in cart:
        price+=int(int(i['price'])*int(i['quantity']))
    # print(price)
    return price
    
# 8-August-2020
@register.filter
def getsellerphoneno(data):
    phoneno= CustomUser.objects.get(id=int(data)).phoneno
    return phoneno
# end 8-August-2020