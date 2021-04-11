from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('browse_pkgs/', include('browse_pkgs.urls')),
    path('admin/', admin.site.urls),
]