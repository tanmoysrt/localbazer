from django.db import models
from accounts.models import CustomUser
from PIL import Image

class BuyerProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='buyer')
    address=models.TextField(default='{"address": []}')

    def __str__(self):
         return str(self.user.phoneno)