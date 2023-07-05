from django.contrib import admin
from .models import Category, Listing, FavoriteListing, ReservationListing


class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "id", "location"]


admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(FavoriteListing)
admin.site.register(ReservationListing)
