from datamanagement.models import OrderHistory,ProductData
from rest_framework import serializers


class PendingOrderHistoryDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = [ 'status']

class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductData
        fields= ['id','name','details','price','originofproduct','available','discount','subcategory','photo']

