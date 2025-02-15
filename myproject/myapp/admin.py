from django.contrib import admin
from .models import Bus, Passenger, Booking, Wallet

admin.site.register(Bus)
admin.site.register(Passenger)
admin.site.register(Booking)
admin.site.register(Wallet)