from django.db import models
from buyer.models import BuyerProfile
from datamanagement.variable import REFERRAL_WITHDRAWL

class referralfirst(models.Model):
    user=models.OneToOneField(BuyerProfile,on_delete=models.CASCADE,related_name='referral')
    rewardpoint=models.FloatField(default=0)
    referrerid=models.BigIntegerField(null=True,default=-1)
    freedelivery=models.BooleanField(default=1)
    refertimes=models.BigIntegerField(default=0,null=True)
    def __str__(self):
        return str(self.user.id)


class referralrequest(models.Model):
    userid=models.BigIntegerField()
    phoneno=models.BigIntegerField()
    rewardpoint=models.BigIntegerField()
    option=models.CharField(max_length=20,choices=REFERRAL_WITHDRAWL)
    additionalphoneno=models.BigIntegerField(null=True,default="")
    coupon=models.TextField(default="")
    status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.phoneno)