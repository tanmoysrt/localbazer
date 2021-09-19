from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('513871540dhejcblkdu8bfi/', admin.site.urls),
    path('account/',include('accounts.urls',namespace='accounts')),
    path('',include('buyer.urls',namespace='buyer')),
    path('seller/',include('seller.urls')),
    path('checkout/',include('checkout.urls')),
    path('shopqr/',include('shopqrhandler.urls')), 
    path('api/',include('api.urls')),
    path('admin/',include('adminpanel.urls')),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = "LocalBazer Admin"
admin.site.site_title = "LocalBazer Admin Portal"
admin.site.index_title = "Welcome to LocalBazer Portal"
