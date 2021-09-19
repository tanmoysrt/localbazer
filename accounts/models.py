from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    first_name=None
    last_name=None
    email = models.EmailField(_('email address'))
    phoneno=models.BigIntegerField(_('phone no'),unique=True)
    name=models.CharField(max_length=50,default='No_NAME')
    userflag=models.BooleanField(default=False)
    USERNAME_FIELD = 'phoneno'
    REQUIRED_FIELDS = ['userflag','email','name']
    verified=models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phoneno)

class PhoneOtp(models.Model):
    phoneno=models.BigIntegerField()
    otp=models.IntegerField()
    count=models.IntegerField(default=3)
    message=models.TextField(default='error')
    def __str__(self):
        return f"{self.phoneno} has sent otp : {self.otp}"

class OtpDirectory(models.Model):
    phoneno=models.BigIntegerField()
    otp=models.IntegerField()
    def __str__(self):
        return f"{self.phoneno} has sent otp : {self.otp}"