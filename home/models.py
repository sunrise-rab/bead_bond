from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BeadType(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/beads/", blank=True, null=True)
    is_included = models.BooleanField(default=True)
    colour = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.name

class Accessory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/accessories/", blank=True, null=True)
    is_included = models.BooleanField(default=True)

    def __str__(self):
        return self.name

