from django.db import models
from datamanagement.models import ProductData,OrderHistory
from datamanagement.variable import ELECTRONICS_CATEGORY,FOOD_CATEGORY,GARMENTS_CATEGORY,GROCERY_CATEGORY,HANDCRAFTS_CATEGORY
from accounts.models import CustomUser
from seller.models import SellerProfile
from django import template
from buyer.models import BuyerProfile
import json

register = template.Library()


@register.filter
def gettotalproductsofshop(data):
    count=len(ProductData.objects.filter(seller_id=int(data)))
    return count

@register.filter
def gettotalordersofshop(data):
    count = len(OrderHistory.objects.filter(sellerid=int(data)))
    return count

@register.filter
def gettotalordersofbuyer(data):
    try:
        count=len(OrderHistory.objects.filter(buyer_id=int(data)))
        return count
    except:
        return 0

@register.filter
def productNameFromId(data):
    product=ProductData.objects.filter(id=int(data))[0]
    name=product.name
    return name

@register.filter
def customerphonefrombuyerid(data):
    x=CustomUser.objects.get(id=int(BuyerProfile.objects.get(id=data).user_id))
    return x.phoneno

@register.filter
def customernamefrombuyerid(data):
    x=CustomUser.objects.get(id=int(BuyerProfile.objects.get(id=data).user_id))
    return x.name

@register.filter
def customeraddressfrombuyerid(data,arg):
    y=json.loads(BuyerProfile.objects.get(id=int(data)).address)
    for i in y["address"]:
        if  int(i["id"]) == int(arg):
            return i["address"]

@register.filter
def getshopnamebysellerid(data):
    x=CustomUser.objects.get(id=int(data)).seller
    return x.shopname
@register.filter
def getshopphonenobysellerid(data):
    x=CustomUser.objects.get(id=int(data))
    return x.phoneno

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
def getCustomerNameFromPhoneno(data):
    try:
        user=CustomUser.objects.get(phoneno=data)
        return user.name
    except:
        return "Not Exsists"