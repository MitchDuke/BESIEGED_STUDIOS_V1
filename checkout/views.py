from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import stripe
from basket.context_processors import basket_context

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Renders the checkout page with items in the basket."""
    context = basket_context(request)
    print("CHECKOUT PAGE BASKET CONTEXT:", context)
    return render(request, "checkout/checkout.html", context)


def create_checkout_session(request):
    """Creates a Stripe Checkout session."""
    basket = request.session.get("basket", {})

    if not basket:
        return redirect("basket:basket_view") # Redirects to basket if is empty

    line_items = []
    for pk, quantity in basket.items():
        line_items.append({
            "price_data": {
                "currency": "gbp",
                "product_data": {
                    "name": f"Project {pk}",
                },
                "unit_amount": 1000,
            },
            "quantity": quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/checkout/success/"),
        cancel_url=request.build_absolute_uri("/checkout/cancel/"),
    )

    return JsonResponse({"session_id": session.id})


def checkout_success(request):
    """Handles a successful payment."""
    request.session["basket"] = {} # Clears the basket after a successful payment
    return render(request, "checkout/success.html")


def checkout_cancel(request):
    """Handles a cancelled payment."""
    return render(request, "checkout/cancel.html")
