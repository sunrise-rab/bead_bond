from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    consent_to_contact = models.BooleanField(default=False)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.email}"
