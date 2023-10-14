from rest_framework import serializers
from rest_framework import filters

from animeapp.models import *


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name',)

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        fields = '__all__'




class AnimeListSerializer(serializers.ModelSerializer):
    gener = GenresSerializer(many=True, read_only=True)
    seasons = SeasonSerializer(many=True, read_only=True)

    class Meta:
        model = AnimeList
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


class AnimeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeRating
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        anime = data.get('anime')

        # Check if the user has already rated the anime
        if AnimeRating.objects.filter(user=user, anime=anime).exists():
            raise serializers.ValidationError("You have already rated this anime.")

        return data
