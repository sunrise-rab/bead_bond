from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Booking
from .forms import BookingForm, BookingChildFormSet
from django.http import JsonResponse
from django.template.loader import render_to_string


@login_required
def my_bookings(request):
    bookings = request.user.bookings.all().order_by("-created_at")
    return render(request, "bookings/my_bookings.html", {"bookings": bookings})


@login_required
def create_booking(request):
    if request.method == "POST":
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.save()

            child_formset = BookingChildFormSet(request.POST, instance=booking)
            if child_formset.is_valid():
                # Stop saving if user submits with all child rows empty
                has_any_child = False
                for f in child_formset.forms:
                    if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                        name = f.cleaned_data.get("name")
                        age = f.cleaned_data.get("age")
                        if name and age is not None:
                            has_any_child = True
                            break

                if not has_any_child:
                    booking.delete()
                    messages.error(request, "Please add at least one child.")
                    return render(
                        request,
                        "bookings/create_booking.html",
                        {"booking_form": booking_form, "child_formset": child_formset}
                    )

                child_formset.save()
                messages.success(request, "Booking created successfully!")
                return redirect("bookings:my_bookings")

            # if child formset invalid, remove booking to avoid empty booking record
            booking.delete()
        else:
            child_formset = BookingChildFormSet(request.POST)
    else:
        booking_form = BookingForm()
        child_formset = BookingChildFormSet()

    return render(
        request,
        "bookings/create_booking.html",
        {"booking_form": booking_form, "child_formset": child_formset}
    )

def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"
@login_required
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == "POST":
        booking_form = BookingForm(request.POST, instance=booking)
        child_formset = BookingChildFormSet(request.POST, instance=booking)

        if booking_form.is_valid() and child_formset.is_valid():
            # Require at least one child remaining (not deleted)
            remaining = 0
            for f in child_formset.forms:
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                    name = f.cleaned_data.get("name")
                    age = f.cleaned_data.get("age")
                    if name and age is not None:
                        remaining += 1

            if remaining == 0:
                messages.error(request, "A booking must have at least one child.")
                return render(
                    request,
                    "bookings/edit_booking.html",
                    {"booking_form": booking_form, "child_formset": child_formset, "booking": booking}
                )

            booking_form.save()
            child_formset.save()
            messages.success(request, "Booking updated!")
            return redirect("bookings:my_bookings")
    else:
        booking_form = BookingForm(instance=booking)
        child_formset = BookingChildFormSet(instance=booking)

    return render(
        request,
        "bookings/edit_booking.html",
        {"booking_form": booking_form,
         "child_formset": child_formset, 
         "booking": booking
         }
    )

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking cancelled successfully.")

    return redirect("bookings:my_bookings")


