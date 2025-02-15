from django.db import models
from django.contrib.auth.models import User

class Bus(models.Model):
    bus_number = models.CharField(max_length=50, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    operating_days = models.CharField(max_length=100)  # Format: "Mon,Tue,Wed"

    def __str__(self):
        return f"{self.bus_number} - {self.source} to {self.destination}"

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(Passenger)
    booking_date = models.DateTimeField(auto_now_add=True)
    num_tickets = models.PositiveIntegerField(default=1)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.user.username}"