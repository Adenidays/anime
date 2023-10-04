from django.contrib import admin

from userapp.models import *
admin.site.register(User)
admin.site.register(WishList)
admin.site.register(UserSubscription)
admin.site.register(AnimeCollection)