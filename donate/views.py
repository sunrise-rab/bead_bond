from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe
from .models import Donation

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def donate_page(request):
    return render(request, "donate/donate.html", {"stripe_public_key": settings.STRIPE_PUBLIC_KEY})


@require_POST
def create_checkout_session(request):
    """
    Creates a Stripe Checkout Session, stores a Donation row as UNPAID.
    """
    amount = request.POST.get("amount", "10")
    name = request.POST.get("name", "")
    email = request.POST.get("email", "")
    message = request.POST.get("message", "")

    try:
        amount_dec = Decimal(amount)
        if amount_dec <= 0:
            raise ValueError("Amount must be > 0")
    except Exception:
        return JsonResponse({"error": "Invalid amount"}, status=400)

    donation = Donation.objects.create(
        name=name,
        email=email,
        amount_gbp=amount_dec,
        message=message,
        paid=False,
    )

    domain = request.build_absolute_uri("/")[:-1]  # removes trailing slash
    success_url = domain + "/donate/success/?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = domain + "/donate/cancel/"

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": "Bead Bond Donation"},
                "unit_amount": int(amount_dec * 100),
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"donation_id": str(donation.id)},
    )

    donation.stripe_session_id = session.id
    donation.save(update_fields=["stripe_session_id"])

    # For Bootstrap 4 form submit → return JSON and redirect via JS
    return JsonResponse({"id": session.id})


def donate_success(request):
    """
    Marks donation as paid using the Checkout session status (simple approach).
    """
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("donate:donate")

    session = stripe.checkout.Session.retrieve(session_id)

    # paid if payment_status == "paid"
    if session.get("payment_status") == "paid":
        Donation.objects.filter(stripe_session_id=session_id).update(paid=True)

    return render(request, "donate/success.html")


def donate_cancel(request):
    return render(request, "donate/cancel.html")
