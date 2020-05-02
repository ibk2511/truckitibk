from django.contrib import admin
from .models import Truck, Owner, Client, TruckRent

# Register your models here.

admin.site.register(Truck)
admin.site.register(Owner)
admin.site.register(Client)
admin.site.register(TruckRent)
