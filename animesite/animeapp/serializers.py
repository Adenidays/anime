from rest_framework import serializers
from rest_framework import filters

from animeapp.models import *


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name',)


class AnimeListSerializer(serializers.ModelSerializer):
    gener = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = AnimeList
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class GenreFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre_names = request.query_params.getlist('genre')
        if genre_names:
            queryset = queryset.filter(gener__name__in=genre_names)
        return queryset
