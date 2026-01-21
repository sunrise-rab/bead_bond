from django.db import models

# Create your models here.
from django.db import models

class Donation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    amount_gbp = models.DecimalField(max_digits=7, decimal_places=2)
    message = models.TextField(blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"£{self.amount_gbp} - {'PAID' if self.paid else 'UNPAID'}"
