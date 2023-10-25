from django.urls import path

from userapp.views import *

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-username/',ChangeUsernameView.as_view(), name='change-username')
]
