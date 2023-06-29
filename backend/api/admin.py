from django.contrib import admin
from .models import Category, Listing, FavoriteListing


admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(FavoriteListing)
