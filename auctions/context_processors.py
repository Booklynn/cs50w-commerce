def watchlist_count(request):
    if request.user.is_authenticated:
        filtered_active_listings = [listing for listing in request.user.watchlist.all() if listing.listing.active]
        watchlist_count = len(filtered_active_listings)
    else:
        watchlist_count = 0
    
    return {
        'watchlist_count': watchlist_count
    }
