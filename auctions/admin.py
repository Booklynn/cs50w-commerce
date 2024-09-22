from django.contrib import admin

from auctions.models import AuctionListing, Bid

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "image_url", "category", "date", "active", "owner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "amount", "bidder", "date")

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)