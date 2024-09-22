from django.contrib import admin

from auctions.models import AuctionListing, Bid, Comment, Watchlist

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "starting_bid", "image_url", "category", "date", "active", "owner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "amount", "bidder", "date")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "comment", "date")

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment, CommentAdmin)