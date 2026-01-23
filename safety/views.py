from django.shortcuts import render

# Create your views here.


def health_safety(request):
    return render(request, "safety/health_safety.html")
