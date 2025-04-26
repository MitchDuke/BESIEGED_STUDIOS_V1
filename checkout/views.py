from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import stripe
from basket.context_processors import basket_context
from .models import Order, OrderItem
from gallery.models import Project
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Renders the checkout page with items in the basket."""
    context = basket_context(request)
    print("CHECKOUT PAGE BASKET CONTEXT:", context)
    return render(request, "checkout/checkout.html", context)


def create_checkout_session(request):
    """Creates a Stripe Checkout session with correct user/basket data."""
    if request.method == "POST":
        # Get user details from the form
        full_name = request.POST.get("fullName")
        email = request.POST.get("email")
        house_number = request.POST.get("houseNumber")
        street = request.POST.get("street")
        address_line2 = request.POST.get("addressLine2", "")
        town = request.POST.get("town")
        postcode = request.POST.get("postcode")

        # Save basic checkout info into session immediately
        request.session["full_name"] = full_name
        request.session["email"] = email
        request.session["address"] = f"{house_number} {street}, {address_line2}, {town}, {postcode}"

        # Get the basket
        basket = request.session.get("basket", {})

        if not basket:
            messages.error(request, "Your basket is empty.")
            return redirect("basket:basket_view")

        line_items = []
        for pk, quantity in basket.items():
            try:
                project = Project.objects.get(pk=int(pk))
                price_in_pence = int(project.price * 100)
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
            except Project.DoesNotExist:
                continue  # Ignore missing projects safely

        try:
            # Create the Stripe session
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

            # Save the Stripe session ID immediately after creation
            request.session["stripe_session_id"] = session.id

            # Redirect user straight to Stripe hosted page
            return redirect(session.url, code=303)

        except Exception as e:
            print(f"Stripe session error: {str(e)}")
            messages.error(request, "There was an error starting your payment session. Please try again.")
            return redirect("checkout:checkout")

    return redirect("checkout:checkout")


def checkout_success(request):
    basket = request.session.get("basket", {})
    user = request.user if request.user.is_authenticated else None

    if basket:
        full_name = request.session.get("full_name", "Guest")
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
                project = Project.objects.get(pk=int(pk))
                OrderItem.objects.create(order=order, project=project, quantity=qty)
            except Project.DoesNotExist:
                continue

    # Clear basket
    request.session["basket"] = {}

    # Clean up checkout details from session
    for key in ["full_name", "email", "address", "stripe_session_id"]:
        request.session.pop(key,None)

    if request.user.is_authenticated:
        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect('dashboard')  # Go to dashboard if logged in
    else:
        return render(request, "checkout/success.html")


def checkout_cancel(request):
    """Handles a cancelled payment."""
    return render(request, "checkout/cancel.html")
