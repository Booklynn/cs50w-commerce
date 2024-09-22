from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from auctions.helpers import get_current_bidder, has_user_won_auction, is_in_watchlist, is_user_owning_listing

from .models import AuctionListing, User


def index(request):
    category_name = request.GET.get('category')
    if category_name:
        auctions = AuctionListing.objects.filter(category=category_name).exclude(active=False)
    else:
        auctions = AuctionListing.objects.all().exclude(active=False)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create_listing_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting-bid"]
        image_url = request.POST["image-url"]
        category = request.POST["category"]
        owner = request.user

        try:
            listing = AuctionListing.objects.create(
                title=title,
                description=description,
                starting_bid=starting_bid,
                image_url=image_url,
                category=category,
                owner=owner
            )
            listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Error creating listing."
            })
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/create_listing.html")


def listing_view(request, listing_id):
    current_listing = AuctionListing.objects.get(pk=listing_id)
    bid_count = current_listing.bids.count()
    current_bidder = get_current_bidder(current_listing)
    in_watchlist = is_in_watchlist(request.user, current_listing)
    comments = current_listing.comments.all()
        
    if is_user_owning_listing(request.user, current_listing.owner):
        display_message = "You are the creator of this listing."
    elif has_user_won_auction(request.user, current_listing):
        display_message = "Congratulations, you've won the auction!"
    elif not current_listing.active:
        display_message = "This auction is closed."
    else:
        display_message = None

    return render(request, "auctions/listing.html", {
        "listing": current_listing,
        "bid_count": bid_count,
        "current_bidder": current_bidder,
        "display_message": display_message,
        "in_watchlist": in_watchlist,
        "comments": comments
    })


@login_required(login_url='/login')
def bid(request, listing_id):
    if request.method == "POST":
        bid_amount = request.POST["bid"]
        current_listing = AuctionListing.objects.get(pk=listing_id)
        in_watchlist = is_in_watchlist(request.user, current_listing)

        if current_listing.owner == request.user and current_listing.active:
            return render(request, "auctions/listing.html", {
                "listing": current_listing,
                "bid_count": current_listing.bids.count(),
                "current_bidder": get_current_bidder(current_listing),
                "message": "You can't bid on your own listing.",
                "in_watchlist": in_watchlist
            })
        
        if Decimal(bid_amount) > current_listing.starting_bid and current_listing.active:
            try:
                current_listing.bids.create(
                    listing=current_listing,
                    amount=bid_amount,
                    bidder=request.user
                )

                current_listing.starting_bid = bid_amount
                current_listing.save()

                messages.success(request, "Bid placed successfully.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            
            except IntegrityError:
                return render(request, "auctions/listing.html", {
                    "listing": current_listing,
                    "bid_count": current_listing.bids.count(),
                    "current_bidder": get_current_bidder(current_listing),
                    "message": "Error bidding this listing.",
                    "in_watchlist": in_watchlist
                })
        
        messages.info(request, "Bid must be higher than the current bid.")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='/login')
def close_auction(request, listing_id):
    if request.method == "POST":
        current_listing = AuctionListing.objects.get(pk=listing_id)
        
        if request.user == current_listing.owner and current_listing.active:
            if not current_listing.bids.exists():
                messages.info(request, "No bids to close this auction.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

            try:
                current_listing.active = False
                current_listing.save()

                messages.success(request, "Auction closed successfully.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            
            except IntegrityError:
                messages.error(request, "Error closing this auction.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='/login')
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        current_listing = AuctionListing.objects.get(pk=listing_id)
        
        try:
            if is_in_watchlist(request.user, current_listing) and current_listing.active:
                request.user.watchlist.get(listing=current_listing).delete()    
                messages.success(request, "Listing removed from your watchlist.")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
            request.user.watchlist.create(listing=current_listing)
            messages.success(request, "Listing added to your watchlist.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        except IntegrityError:
            messages.error(request, "Error adding this listing to your watchlist.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required(login_url='/login')
def watchlist_view(request):
    watchlists = request.user.watchlist.all()
    filtered_active_watchlists = [item for item in watchlists if item.listing.active]

    return render(request, "auctions/watchlist.html", {
        "watchlists": filtered_active_watchlists
    })


@login_required(login_url='/login')
def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        current_listing = AuctionListing.objects.get(pk=listing_id)
        
        try:
            current_listing.comments.create(
                user=request.user,
                comment=comment
            )
            messages.success(request, "Comment added successfully.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        except IntegrityError:
            messages.error(request, "Error adding comment.")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def categories(request):
    categories = AuctionListing.objects.values_list("category", flat=True).distinct().exclude(category="").exclude(active=False)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })