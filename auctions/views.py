from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import AuctionListing, User


def index(request):
    return render(request, "auctions/index.html", {
        "auction_list": AuctionListing.objects.all().exclude(active=False)
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
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
    })