from django.contrib import admin

from auctions.models import AuctionListing

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "image_url", "category", "date", "active", "owner")

admin.site.register(AuctionListing, AuctionListingAdmin)