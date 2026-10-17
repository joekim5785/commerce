from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    pass

User = get_user_model()
class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=64, blank=True)
    starting_bid = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.URLField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.description} :{self.starting_bid} :{self.category} :{self.image}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing= models.ForeignKey(Listings, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.listing} :{self.added_at}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing= models.ForeignKey(Listings, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bidder}: {self.listing} :{self.amount}:{self.bid_time}:{self.winner}"

class Comments(models.Model):
    comment=models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing= models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}:{self.user}: {self.listing}:{self.comment_date}"
