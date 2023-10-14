from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animeapp.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path(f'^auth/', include('djoser.urls.authtoken')),
]
