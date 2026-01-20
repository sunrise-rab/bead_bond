from django.db import models
from django.contrib.auth.models import User




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    photo_consent = models.BooleanField(default=False)
    notes = models.TextField(blank=True)  # optional: allergies/support etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.pk} - {self.booking_date}"


class BookingChild(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="children")
    name = models.CharField(max_length=80)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.age})"
