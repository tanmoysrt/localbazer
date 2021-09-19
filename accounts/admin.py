from django.contrib import admin
from .models import CustomUser,PhoneOtp,OtpDirectory
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from seller.models import SellerProfile
# Unregister Group Section
admin.site.unregister(Group)


# Custom Admin Page For Account- User Model
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('name', 'email','phoneno','date_joined','userflag','is_active','verified')
    list_filter = ('userflag','is_active')
    fieldsets = (
        (None, {'fields': ('name','phoneno','email','userflag','date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','phoneno','email', 'password1', 'password2', 'userflag')}
        ),
    )
    search_fields = ('email','phoneno','name')
    ordering = ('date_joined',)
    def make_active(modeladmin, request, queryset): 
        queryset.update(is_active = 1) 
        messages.success(request, "Selected Record(s) Marked as Active Successfully !!") 
  
    def make_inactive(modeladmin, request, queryset): 
        queryset.update(is_active = 0) 
        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!") 
  
    admin.site.add_action(make_active, "Make Active") 
    admin.site.add_action(make_inactive, "Make Inactive") 
    def has_add_permission(self, request): 
        return False
# Register Account- User Model
admin.site.register(CustomUser, CustomUserAdmin)
class SellerCustom(admin.ModelAdmin):
	list_filter = ('shopcategoty','allindia','homedelivery')
	list_display = ('shopname','user','shopaddress','shopcategoty','allindia','homedelivery')
admin.site.register(SellerProfile,SellerCustom)
admin.site.register(PhoneOtp)
admin.site.register(OtpDirectory)
# admin.site.register(FCMTokenDirectory)