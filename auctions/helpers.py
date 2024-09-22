def get_current_bidder(listing):
    return listing.bids.last().bidder if listing.bids.exists() else None

def is_user_owning_listing(current_user, listing_owner):
    return current_user == listing_owner

def has_user_won_auction(current_user, current_listing):
    if not current_listing.active:
        current_bidder = get_current_bidder(current_listing)
        return current_user == current_bidder

def is_in_watchlist(current_user, current_listing):
    return current_user.watchlist.filter(listing=current_listing).exists()