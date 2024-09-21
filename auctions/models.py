from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=64, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

# class Bid(models.Model):
#     pass

# class Comment(models.Model):
#     pass