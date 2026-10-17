from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max

from .models import User, Listings, Watchlist, Bid, Comments

# listing form


class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    starting_bid = forms.DecimalField(label="Starting bid")
    category = forms.CharField(label="Category",required=False)
    image = forms.URLField(label="Image URL", required=False)


class BidForm(forms.Form):
    bid = forms.DecimalField(label="Bid", max_digits=10, decimal_places=2)


class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)


def index(request):

    listings = Listings.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings,
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


@login_required
def createlisting(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = Listings(
                title=form.cleaned_data["title"].title(),
                description=form.cleaned_data["description"].title(),
                category=form.cleaned_data["category"].title(),
                starting_bid=form.cleaned_data["starting_bid"],
                image=form.cleaned_data["image"],
                owner=request.user,
            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createlisting.html", {
        "form": CreateListingForm()
    })



def listing(request, id):

    listing = Listings.objects.get(id=id)

    comments = Comments.objects.filter(listing=listing)

    if request.user.is_authenticated:
        watchlist_exists = Watchlist.objects.filter(
            listing=listing,
            user=request.user
        ).exists()
    else:
        watchlist_exists = False

    bidder = Bid.objects.filter(listing=listing)

    winning_bid = Bid.objects.filter(
        listing=listing,
        winner=True
    ).first()

    owner = listing.owner

    return render(request, "auctions/viewlisting.html", {
        "listing": listing,
        "owner": owner,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "comments": comments,
        "bidder": bidder,
        "winning_bid": winning_bid,
        "watchlist_exists": watchlist_exists,
    })

@login_required
def add_to_watchlist(request, id):
    listing = Listings.objects.get(id=id)
    watchlist = Watchlist(
        user=request.user,
        listing=listing,
    )
    watchlist.save()

    return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def watchlist(request):
    watchlists = Watchlist.objects.filter(user_id=request.user.id)

    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists,
        })

@login_required
def remove_from_watchlist(request,id):
    listing = Listings.objects.get(id=id)
    watchlist = Watchlist.objects.get(user=request.user.id,listing=listing)
    remove = Watchlist(
        watchlist.id
    )
    remove.delete()

    return HttpResponseRedirect(reverse("index"))



def category(request):
    listings = Listings.objects.values("category").distinct()

    return render(request, "auctions/categories.html", {
        "listings": listings,
    })


def view_category(request, category):
    listings = Listings.objects.filter(category=category)
    return render(request, "auctions/view_listing_category.html", {
        "listings": listings
    })


def bid(request, id):
    listing = Listings.objects.get(id=id)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["bid"]
            highest_bid = Bid.objects.filter(listing_id=id).aggregate(Max("amount"))["amount__max"]

            if amount < listing.starting_bid:
                message = "The bid must be at least the starting bid"
            elif highest_bid is not None and amount <= highest_bid:
                message = "Your bid must be higher than the current highest bid"
            else:
                Bid(bidder=request.user, listing=listing, amount=amount).save()
                return HttpResponseRedirect(reverse("listing", args=[id]))

            return render(request, "auctions/viewlisting.html", {
                "listing": listing,
                "bid_form": form,
                "message": message,
            })

    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def close_auction(request, id):
    user = request.user
    listing = Listings.objects.get(id=id)
    if user == listing.owner:
        listing.is_active = False
        listing.save()
        highest_bid = Bid.objects.filter(
            listing_id=id
        ).order_by("-amount").first()


        if highest_bid is not None:
            highest_bid.winner = True
            highest_bid.save()

    return HttpResponseRedirect(reverse("index"))


@login_required
def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():

            add_comment = Comments(
                comment=form.cleaned_data["comment"],
                user=request.user,
                listing=Listings.objects.get(id=id),

            )
            add_comment.save()

            return HttpResponseRedirect(reverse("listing", args=[id]))

    return HttpResponseRedirect(reverse("listing", args=[id]))


