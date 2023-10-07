import django_filters

from animeapp.models import AnimeList


class AnimeListFilter(django_filters.FilterSet):
    genres = django_filters.CharFilter(method='filter_genres')

    class Meta:
        model = AnimeList
        fields = ['genres']

    def filter_genres(self, queryset, name, value):
        genres = value.split(',')

        return queryset.filter(gener__name__in=genres).distinct()
