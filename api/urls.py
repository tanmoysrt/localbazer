from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('pending/', views.PendingOrders.as_view()),
    path('pending/<int:id>', views.PendingOrdersDetails.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('buyerdata/<int:pk>/<int:addressid>', views.BuyerDetails.as_view()),
    path('add/', views.AddProduct.as_view()),
    path('product/<int:id>', views.ProductDataAPI.as_view()),
    path('registerfcm/',views.registerFCM)
]

