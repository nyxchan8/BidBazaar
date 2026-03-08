from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Auction, Category, Bid, Comment, User
from decimal import Decimal

def index(request):
    listings = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
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
    
def detail(request, id):

    listing = get_object_or_404(Auction, pk=id)

    comments = Comment.objects.filter(auction=listing).order_by("created_at")

    highest_bid = Bid.objects.filter(auction=listing).aggregate(Max("amount"))["amount__max"]

    if highest_bid is None:
        highest_bid = listing.starting_bid

    if request.method == "POST" and request.user.is_authenticated:

        # COMMENT
        if "comment_text" in request.POST:
            text = request.POST.get("comment_text").strip()
            if text:
                Comment.objects.create(
                    auction=listing,
                    user=request.user,
                    text=text
                )
            return redirect("detail", id=id)

        # BID
        if "bid" in request.POST:
            bid = float(request.POST.get("bid"))

            if bid <= highest_bid:
                messages.error(request, "Your bid must be higher than the current bid.")
            else:
                Bid.objects.create(
                    auction=listing,
                    user=request.user,
                    amount=bid
                )
                messages.success(request, "Bid placed successfully!")
                return redirect("detail", id=id)

    return render(request, "auctions/detail.html", {
        "listing": listing,
        "comments": comments,
        "highest_bid": highest_bid
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    items = Auction.objects.filter(category=category_obj)
    return render(request, "auctions/category.html", {
        "category": category_obj,
        "items": items
    })

@login_required
def new_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    categories = Category.objects.all() 

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = Decimal(request.POST.get("starting_bid"))
        image = request.POST.get("image")
        category_id = request.POST.get("category")

        category = Category.objects.get(pk=category_id) if category_id else None

        auction = Auction.objects.create(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image=image,
            category=category,
            creator=request.user
        )

        return redirect("detail", id=auction.id)

    return render(request, "auctions/listing.html", {
        "categories": categories
    })

@login_required
def watchlist_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    listings = request.user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def watchlist_toggle(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    listing = get_object_or_404(Auction, pk=id)

    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
    else:
        listing.watchlist.add(request.user)

    return redirect("detail", id=id)

@login_required
def endlist(request): 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
           
    closes = Auction.objects.filter(
        status=Auction.Status.CLOSED,
        creator=request.user
    )
    
    return render(request, "auctions/end.html", {
        "closes": closes,
    })

@login_required
def endlist_toggle(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    listing = get_object_or_404(Auction, pk=id)

    if request.user != listing.creator:
        return redirect("detail", id=id)

    if request.method == "POST":

        highest_bid = Bid.objects.filter(auction=listing).order_by("-amount").first()

        if highest_bid:
            listing.winner = highest_bid.user

        listing.status = Auction.Status.CLOSED
        listing.save()

    return redirect("detail", id=id)
