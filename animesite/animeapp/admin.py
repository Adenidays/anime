from django.contrib import admin

from animeapp.models import *

admin.site.register(AnimeList)
admin.site.register(Genres)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Comment)
