from django.contrib import admin
from .models import ProductData,OrderHistory,PriceDefinitionsForDelivery,FCMTokenDirectory

class productdatacustom(admin.ModelAdmin):
	model=ProductData
	list_filter = ('subcategory','originofproduct')
	list_display = ('name','price','available','discount','subcategory','originofproduct','seller')
	list_per_page = 20

class OrderHistoryCustom(admin.ModelAdmin):
	model=OrderHistory
	list_display=('id','sellerid','buyer_id','orderedon')

admin.site.register(ProductData,productdatacustom)
admin.site.register(OrderHistory,OrderHistoryCustom)
admin.site.register(PriceDefinitionsForDelivery)
admin.site.register(FCMTokenDirectory)