from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animeapp.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path(f'^auth/', include('djoser.urls.authtoken')),
    path('api/auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include('userapp.urls'))
]
