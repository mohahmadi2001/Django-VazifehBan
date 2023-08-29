from django.contrib import admin
from django.urls import path, include,re_path


urlpatterns = [
    re_path(r"^auth/", include("accounts.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
]

