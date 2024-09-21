from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class CreateListing(models.Model):
    pass

class AuctionListing(models.Model):
    pass

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass