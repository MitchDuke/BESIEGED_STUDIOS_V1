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

        # SAVE these into session before creating Stripe session!
        request.session["full_name"] = full_name
        request.session["email"] = email
        request.session["address"] = f"{house_number} {street}, {address_line2}, {town}, {postcode}"

        # Retrieve basket from session
        basket = request.session.get("basket", {})

        if not basket:
            return redirect("basket:basket_view")

        # Prepare Stripe line items
        line_items = []
        for pk, quantity in basket.items():
            try:
                project = Project.objects.get(pk=int(pk))
                price_in_pence = int(project.price * 100)
            except Project.DoesNotExist:
                continue

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

            # Also store session ID so we can link it later
            request.session["stripe_session_id"] = session.id

            return redirect(session.url)

        except Exception as e:
            print("Stripe Error:", str(e))
            return redirect("checkout:checkout")

    return redirect("checkout:checkout")


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
