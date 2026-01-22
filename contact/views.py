from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

# Create your views here.


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("contact:contact")
        messages.error(request, "Please check the form and try again.")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
