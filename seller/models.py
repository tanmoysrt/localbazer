from django.db import models
from accounts.models import CustomUser
from datamanagement.variable import CATAGORY_CHOICE
from PIL import Image

class SellerProfile(models.Model):
    user=models.OneToOneField(CustomUser,related_name='seller',on_delete=models.CASCADE)
    shopname=models.CharField(max_length=50,default="Unnamed Shop")
    shopaddress=models.CharField(max_length=200,null=True)
    shoplongitude=models.FloatField(null=True,default=0)
    shoplatitude=models.FloatField(null=True,default=0)
    shoppincodes=models.CharField(max_length=200,default=[])
    shopphoto=models.ImageField(upload_to='shop/photo',default='default/shopphotor.jpg')
    shopbanner=models.ImageField(upload_to='shop/banner',default='default/shopbanner.jpg')
    status=models.BooleanField(default=True)
    shopcategoty=models.CharField(max_length=30,null=True,choices=CATAGORY_CHOICE)
    review=models.FloatField(default=5.0)
    homedelivery=models.BooleanField(default=0)   #Available or Not
    deliverycharge=models.FloatField(default=0)   #Delivery Charge if homedeilvery true
    freedelivery=models.BooleanField(default=0)   #Free delvery above some minimum price is true or false 
    minpriceforfreedelivery=models.FloatField(default=499)  #If free delivery true, what will be the minmimum proce for free  delivery
    allindia=models.BooleanField(default=0) #allindia delivery true or false
    ordering_shop = models.IntegerField(default=0,blank=True,null=True)

    def __str__(self):
        return str(self.user.phoneno)
