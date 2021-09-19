from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser

# Classes For Accounts- User Model Django Admin Customization
class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('phoneno','name','email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('phoneno',)