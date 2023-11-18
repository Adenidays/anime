from django.urls import path

from userapp.views import *

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-username/', ChangeUsernameView.as_view(), name='change-username'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('wishlist/', WishListView.as_view(), name='wishlist-list-create'),
    path('users/<int:user_id>/wishlist/', UserWishListView.as_view(), name='user-wishlist'),
    path('create_collection/', AnimeCollectionCreateView.as_view(), name='create-collection'),
    path('collections/', CollectionListView.as_view(), name='collection-list'),#"?popular=true
]
