from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.dashboard,name='admin'),
    path('login/',views.adminlogin),
    path('logout/',views.logoutt),
    path('orders/pending/',views.pendingorders,name="adminpendingorders"),
    path('orders/deilvered/', views.deliveredorders, name="admindeliveredorders"),
    path('orders/cancelled',views.cancelledorders,name="admincancelledorders"),
    path('registration/buyer/',views.buyerregistration,name="adminbuyerregistration"),
    path('registration/seller/',views.sellerregistration,name="adminsellerregistration"),
    path('profile/seller/',views.sellerprofiles,name="adminsellerprofiles"),
    path('profile/buyer/',views.buyerprofiles,name="adminbuyerprofiles"),
    path('orders/data/',views.orderdata),
    path('gateway/sms/',views.smsgateway,name="adminsmsgateway"),
    path('logs/order/',views.orerlogs,name="adminorderlogs"),
    path('logs/newotp/',views.newotp,name="adminnewotplogs"),
    path('logs/resetotp/',views.resetotp,name='adminresetotp'),
    path('logs/qrcodelogs',views.qrcodes,name='adminqrcodelogs'),
]
