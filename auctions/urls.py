from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("RemoveFromWatchlist/<int:id>", views.remove_from_watchlist, name="RemoveFromWatchlist"),
    path("AddToWatchlist/<int:id>", views.add_to_watchlist, name="AddToWatchlist"),
    path("ViewCategory/<str:category>", views.view_category, name="view_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("CloseAuction/<int:id>", views.close_auction, name="close_auction"),
    path("comment/<int:id>", views.comment, name="comment"),
]

