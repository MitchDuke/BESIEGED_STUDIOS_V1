from django.urls import path
from . import views
from . import webhooks

app_name = "checkout"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.checkout_success, name="checkout_success"),
    path("cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("webhook/stripe/", webhooks.stripe_webhook, name="stripe_webhook"),
]
