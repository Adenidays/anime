from rest_framework import filters


class GenreFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        genre_name = request.query_params.get('genre')
        if genre_name:
            queryset = queryset.filter(gener__name=genre_name)
        return queryset


class TypeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        anime_type = request.query_params.get('type')
        if anime_type:
            queryset = queryset.filter(type=anime_type)
        return queryset

