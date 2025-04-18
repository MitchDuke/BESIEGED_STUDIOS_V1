from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import stripe
from basket.context_processors import basket_context
from .models import Order, OrderItem
from gallery.models import Project

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Renders the checkout page with items in the basket."""
    context = basket_context(request)
    print("CHECKOUT PAGE BASKET CONTEXT:", context)
    return render(request, "checkout/checkout.html", context)


def create_checkout_session(request):
    """Creates a Stripe Checkout session with the correct prices."""
    if request.method == "POST":
        # Get user details from the form
        full_name = request.POST.get("fullName")
        email = request.POST.get("email")
        house_number = request.POST.get("houseNumber")
        street = request.POST.get("street")
        address_line2 = request.POST.get("addressLine2", "")
        town = request.POST.get("town")
        postcode = request.POST.get("postcode")

        # Validate required fields
        if not all([full_name, email, house_number, street, town, postcode]):
            return redirect("checkout:checkout")  # Redirect back if form incomplete

        # Retrieve basket from session
        basket = request.session.get("basket", {})

        if not basket:
            return redirect("basket:basket_view")  # Redirect if basket empty

        # Prepare Stripe line items with correct pricing
        line_items = []
        for pk, quantity in basket.items():
            try:
                project = Project.objects.get(pk=int(pk))  # Get the correct project
                price_in_pence = int(project.price * 100)  # Convert price to pence
            except Project.DoesNotExist:
                continue  # Skip items that don't exist

            line_items.append({
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": project.title,
                    },
                    "unit_amount": price_in_pence, 
                },
                "quantity": quantity,
            })

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                customer_email=email,
                billing_address_collection="auto",
                shipping_address_collection=None,
                payment_intent_data={
                    "setup_future_usage": "off_session", # Save card for future payments
                },
                metadata={
                    "full_name": full_name,
                    "house_number": house_number,
                    "street": street,
                    "address_line2": address_line2,
                    "town": town,
                    "postcode": postcode,
                },
                success_url=request.build_absolute_uri("/checkout/success/"),
                cancel_url=request.build_absolute_uri("/checkout/cancel/"),
            )

            # Redirect the user to Stripe for payment
            return redirect(session.url)

        except Exception as e:
            print("Stripe Error:", str(e))  # Debugging
            return redirect("checkout:checkout")  # Redirect back on failure

    return redirect("checkout:checkout")  # Redirect if accessed via GET


def checkout_success(request):
    """Handles a successful payment."""
    basket = request.session.get("basket", {})
    user = request.user if request.user.is_authenticated else None

    if basket:
        # Get last stripe session data
        full_name = request.session.get("full_name", "Guest" )
        email = request.session.get("email", "noemail@example.com")
        address = request.session.get("address", "No address provided")
        session_id = request.session.get("stripe_session_id", "")

        order = Order.objects.create(
            user=user,
            stripe_session_id=session_id,
            full_name=full_name,
            email=email,
            address=address,
        )

        for pk, qty in basket.items():
            try:
                project = Project.objects.get(pk=int(pk))  # Get the correct project
                OrderItem.objects.create(order=order, project=project, quantity=qty)
            except Project.DoesNotExist:
                continue

    request.session["basket"] = {}  # Clears the basket after a successful payment
    return render(request, "checkout/success.html")


def checkout_cancel(request):
    """Handles a cancelled payment."""
    return render(request, "checkout/cancel.html")
