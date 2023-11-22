import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter

from rest_framework.permissions import IsAuthenticated
from animeapp.config import CustomPagination, IsAdminOrStaffUser
from animeapp.filter import GenreFilterBackend, TypeFilterBackend
from animeapp.serializers import *
from rest_framework import viewsets, permissions


class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


def import_data_from_json(request):
    with open('animeapp/AnimeApi.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    for item in data['data']:
        anime = AnimeList(
            title=item['title'],
            episodes=item['episodes'],
            image=item['image'],
            status=item['status'],
            synopsis=item['synopsis'],
            type=item['type'],
            hasEpisode=item['hasEpisode']
        )
        anime.save()

        for genre_name in item['genres']:
            genre, created = Genres.objects.get_or_create(name=genre_name)
            anime.gener.add(genre)

    return render(request, 'import_success.html')


class AnimeListView(generics.ListAPIView):
    serializer_class = AnimeListSerializer
    pagination_class = CustomPagination
    filter_backends = [GenreFilterBackend, TypeFilterBackend, SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        queryset = AnimeList.objects.all()
        top_rated = self.request.query_params.get('top_rated', None)
        if top_rated:
            queryset = queryset.order_by('-rating')[:100]

        return queryset


class AnimeListDetailView(generics.RetrieveAPIView):
    queryset = AnimeList.objects.all()
    serializer_class = AnimeListSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    http_method_names = ['post', 'put', 'delete']
    permission_classes = [IsStaffPermission]


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    http_method_names = ['post', 'put', 'delete']
    permission_classes = [IsStaffPermission]


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_comment_id = self.request.data.get('parent_comment')
        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            serializer.save(user=self.request.user, parent_comment=parent_comment)
        else:
            serializer.save(user=self.request.user)


class AnimeListDeleteView(generics.DestroyAPIView):
    queryset = AnimeList.objects.all()
    serializer_class = AnimeListSerializer
    permission_classes = [IsAdminOrStaffUser]


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrStaffUser]


class SeasonDeleteView(generics.DestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAdminOrStaffUser]


class EpisodeDeleteView(generics.DestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdminOrStaffUser]


class AnimeRatingViewSet(viewsets.ModelViewSet):
    queryset = AnimeRating.objects.all()
    serializer_class = AnimeRatingSerializer
    permission_classes = [IsAuthenticated]


class AnimeTVListViewSet(viewsets.ModelViewSet):
    queryset = AnimeList.objects.filter(type='TV')
    serializer_class = AnimeListSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('gener', 'seasons__episodes', 'comments__user',
                                                       'anime_ratings__user')


class AnimeMovieListViewSet(viewsets.ModelViewSet):
    queryset = AnimeList.objects.filter(type='Movie')
    serializer_class = AnimeListSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('gener', 'seasons__episodes', 'comments__user',
                                                       'anime_ratings__user')
