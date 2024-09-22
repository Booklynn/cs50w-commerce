from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing_view, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close-auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("add-to-watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
