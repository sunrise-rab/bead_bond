from django.urls import path
from . import views

app_name = "donate"

urlpatterns = [
    path("", views.donate_page, name="donate"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.donate_success, name="success"),
    path("cancel/", views.donate_cancel, name="cancel"),
    path("webhook/", views.stripe_webhook, name="webhook"),
]
