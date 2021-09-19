from django.db import models
from accounts.models import CustomUser
from PIL import Image
from .variable import DELIVERY_STATUS_CHOICES
from seller.models import SellerProfile
from buyer.models import BuyerProfile
from sorl.thumbnail import  get_thumbnail

class ProductData(models.Model):
    seller=models.ForeignKey(SellerProfile,on_delete=models.CASCADE,related_name='productdatas')
    name=models.TextField()
    details=models.TextField()
    price=models.FloatField()
    originofproduct=models.CharField(max_length=50)
    available=models.IntegerField()
    review=models.FloatField()
    discount=models.FloatField(default=0)
    subcategory=models.CharField(max_length=20,null=True,blank=True)
    # category=models.CharField(max_length=20)
    photo=models.ImageField(default='default/product.jpg',upload_to='shop/product/')
    def __str__(self):
        return self.name

    @property
    def give_total_price(self):
        total = self.price
        if self.discount != 0:
            total = self.price - self.price * (self.discount / 100)
        return total
class OrderHistory(models.Model):
    buyer=models.ForeignKey(BuyerProfile,on_delete=models.CASCADE,related_name='orderhistories')
    address=models.IntegerField()
    orderedon=models.DateTimeField(auto_now_add=True)
    deliverdon=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=20,choices=DELIVERY_STATUS_CHOICES,default='pending')
    details=models.TextField(null=True)
    sellerid=models.CharField(max_length=500,null=True)
    homedelivery=models.BooleanField(default=False)

    def __str__(self):
        return f'Ordered On {self.orderedon}'


class AllIndiaPinCode(models.Model):
    officename = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    officetype = models.TextField(db_column='officeType', blank=True, null=True)  # Field name made lowercase.
    deliverystatus = models.TextField(db_column='Deliverystatus', blank=True, null=True)  # Field name made lowercase.
    divisionname = models.TextField(blank=True, null=True)
    regionname = models.TextField(blank=True, null=True)
    circlename = models.TextField(blank=True, null=True)
    taluk = models.TextField(db_column='Taluk', blank=True, null=True)  # Field name made lowercase.
    districtname = models.TextField(db_column='Districtname', blank=True, null=True)  # Field name made lowercase.
    statename = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_india_pin_code'


class PriceDefinitionsForDelivery(models.Model):
    ruleName = models.CharField(null=True,default="",max_length=100)
    basePricePerKm = models.FloatField(null=True,default = 0.0)
    basePriceAvailableForRangeInKm = models.FloatField(null=True,default=0.0)
    extraPricePerKm = models.FloatField(null=True,default=0.0)
    pincodeOverride = models.IntegerField(blank=True,null=True)
    priceHikeByTimeStatus = models.BooleanField(null=True,default=False)
    priceHikeAfterTime = models.TimeField(null=True,blank=True)
    additionalCostForPriceHike = models.IntegerField(null=True,default=0,blank=True)

    def __str__(self):
        return self.ruleName

    def save(self, *args, **kwargs):
        if self.pincodeOverride is not None :
            self.ruleName = self.ruleName+str(self.pincodeOverride)
        super(PriceDefinitionsForDelivery , self).save(*args, **kwargs)

class FCMTokenDirectory(models.Model):
    phoneNo = models.TextField(default="",null=True)
    fcmtoken = models.TextField(default="",null=True)

    def __str__(self):
        return self.phoneNo