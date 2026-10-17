from django.contrib import admin
from .models import Listings,Watchlist,User,Bid,Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comments)
