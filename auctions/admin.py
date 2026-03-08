from django.contrib import admin
from .models import User, Category, Auction, Bid, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name" )
    search_fields = ("username", "email", "first_name", "last_name")
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "creator",
        "starting_bid",
        "status"
    )
    list_filter = ("status", "category")
    search_fields = ("title", "description", "creator__username")
    filter_horizontal = ("watchlist",)  # for ManyToManyField

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "amount", "time")
    list_filter = ("auction", "user")
    search_fields = ("auction__title", "user__username")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "text", "created_at")
    list_filter = ("auction", "user")
    search_fields = ("auction__title", "user__username", "text")