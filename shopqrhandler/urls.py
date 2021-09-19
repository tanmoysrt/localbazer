from django.urls import path
from . import views

urlpatterns = [
    path('',views.redirectt),
    path('register/',views.register),
]