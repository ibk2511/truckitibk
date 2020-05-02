from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False, blank=False)
    aadhar_id = models.CharField(max_length=16, null=False, blank=False)

    def __str__(self):
        return self.user.username + " " + self.phone


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, null=False, blank=False)
    aadhar_id = models.CharField(max_length=16, null=False, blank=False)

    def __str__(self):
        return self.user.username + ' ' + self.phone


class Truck(models.Model):
    image = models.ImageField(upload_to='trucks/', default=None, null=True, blank=True)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, default=None)
    model = models.CharField(max_length=20, null=False, blank=False)
    make = models.CharField(max_length=20, null=False, blank=False)
    # description = models.TextField(default=None)
    capacity = models.FloatField(default=0, null=False, blank=False)
    wheels = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    is_rented = models.BooleanField(default=False)
    rate_per_day = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.owner.user.username + ' ' + self.make + ' ' + self.model + ' ' + str(self.is_rented)


class TruckRent(models.Model):
    is_verified = models.BooleanField(default=False)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_required_time = models.DateField(default=None, blank=True, null=True)
    client_drop_time = models.DateField(default=None, blank=True, null=True)
    pickup_time = models.DateField(default=None, blank=True, null=True)
    drop_time = models.DateField(default=None, blank=True, null=True)
    is_dropped = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.truck.owner.user.username + ' <-- owner' + ' ' + self.user.user.username + ' <--Client'


