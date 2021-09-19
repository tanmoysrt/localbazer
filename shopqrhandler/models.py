from django.db import models

class shopqrdata(models.Model):
    qrdata=models.TextField()
    shopid=models.BigIntegerField()
    def __str__(self):
        return str(self.shopid)