from django.urls import path
from userapp.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-username/', ChangeUsernameView.as_view(), name='change-username'),
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('wishlist/', WishListView.as_view(), name='wishlist-list-create'),
    path('users/<int:user_id>/wishlist/', UserWishListView.as_view(), name='user-wishlist'),
    path('create_collection/', AnimeCollectionCreateView.as_view(), name='create-collection'),
    path('collections/', CollectionListView.as_view(), name='collection-list'),#?popular=true
    path('subscribe/', SubscribeToCollectionView.as_view(), name='subscribe-to-collection'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
