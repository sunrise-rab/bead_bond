from django.shortcuts import render
from .models import BeadType, Accessory

# Create your views here.

def index(request):
    """ A view to return the index page"""
    bead_types = BeadType.objects.all()
    accessories = Accessory.objects.all()
    return render(request, "home/index.html", {
        "bead_types": bead_types,
        "accessories": accessories,
    })
