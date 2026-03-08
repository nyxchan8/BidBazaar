from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max

class User(AbstractUser):
    pass

class Category(models.Model):
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    HOME = "Home & Living"
    BOOKS = "Books"
    SPORTS = "Sports"
    TOYS = "Toys"
    BEAUTY = "Beauty"
    AUTOMOTIVE = "Automotive"
    OTHER = "Other"

    CATEGORY_CHOICES = [
        (ELECTRONICS, "Electronics"),
        (FASHION, "Fashion"),
        (HOME, "Home & Living"),
        (BOOKS, "Books"),
        (SPORTS, "Sports"),
        (TOYS, "Toys"),
        (BEAUTY, "Beauty"),
        (AUTOMOTIVE, "Automotive"),
        (OTHER, "Other"),
    ]

    name = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        default=OTHER,
        unique=True
    )

    def __str__(self):
        return self.name

class Auction(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
        related_name="auctions"
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="auctions"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlist"
    )

    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_auctions"
    )

    def __str__(self):
        return self.title
    
    @property
    def current_price(self):
        highest = self.bids.aggregate(Max("amount"))["amount__max"]
        if highest:
            return highest
        return self.starting_bid

class Bid(models.Model):

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="bids",
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid ${self.amount} on {self.auction}"
    
class Comment(models.Model):

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name="comments",
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.auction}"