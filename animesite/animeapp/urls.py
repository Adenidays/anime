from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('api/anime/', AnimeListView.as_view(), name='anime-list'),
    path('api/anime/<int:pk>', AnimeListDetailView.as_view(), name='anime-detail'),
    path('api/anime/seasons/', SeasonViewSet.as_view({'get': 'list', 'post': 'create'}), name='season-list'),
    path('api/anime/episodes/', EpisodeViewSet.as_view({'get': 'list', 'post': 'create'}), name='episode-list'),
    path('api/comments/', CommentCreateAPIView.as_view(), name='comment-create-api'),
    path('anime/delete/<int:pk>/', AnimeListDeleteView.as_view(), name='delete-anime'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete-comment'),
    path('season/delete/<int:pk>/', SeasonDeleteView.as_view(), name='delete-season'),
    path('episode/delete/<int:pk>/', EpisodeDeleteView.as_view(), name='delete-episode'),
    path('anime/vote/', AnimeRatingViewSet.as_view({'post': 'create'}), name='vote'),
    path('anime/animebyTV', AnimeTVListViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('anime/animebyMovie', AnimeMovieListViewSet.as_view({'get': 'list', 'post': 'create'}))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
