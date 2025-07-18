from django.shortcuts import render, redirect
from django.conf import settings
import stripe
from basket.context_processors import basket_context
from .models import Order, OrderItem
from gallery.models import Project
from django.contrib import messages
from django.urls import reverse
from commissions.models import CommissionQuote
from django.core.mail import send_mail
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    """Renders the checkout page with items in the basket."""
    basket = request.session.get('basket', {})
    basket_items = []

    for pk, quantity in basket.items():
        # Try to get a Project first, else check for a CommissionQuote
        try:
            project = Project.objects.get(pk=int(pk))  # Try to get a Project
            basket_items.append({
                "project": project,
                "quantity": quantity,
                "total_price": project.price * quantity,
                "is_commission": False
            })
        except Project.DoesNotExist:
            try:
                commission = CommissionQuote.objects.get(pk=int(pk))  # Try to get a CommissionQuote
                basket_items.append({
                    "project": commission,
                    "quantity": quantity,
                    "total_price": commission.total_price * quantity,
                    "is_commission": True
                })
            except CommissionQuote.DoesNotExist:
                continue  # Skip if neither Project nor CommissionQuote found

    context = {"basket_items": basket_items}
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
            success_url = request.build_absolute_uri(reverse('checkout:checkout_success'))
            cancel_url = request.build_absolute_uri(reverse('checkout:checkout_cancel'))

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
                success_url=success_url,
                cancel_url=cancel_url,
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

        # Create OrderItems for each item in the basket
        total_price = 0  # Initialize total price for the order
        for pk, qty in basket.items():
            try:
                project = Project.objects.get(pk=int(pk))
                order_item = OrderItem.objects.create(
                    order=order,
                    project=project,
                    quantity=qty
                )
                total_price += project.price * qty
                print(f"created OrderItem: {order_item} for {project.title}")
            except Project.DoesNotExist:
                continue

        # Update the order's total price
        order.total_price = total_price
        order.save()

        # Send confirmation email
        send_order_email(order)

    # Clear basket
    request.session["basket"] = {}

    # Clean up checkout details from session
    for key in ["full_name", "email", "address", "stripe_session_id"]:
        request.session.pop(key, None)

    if request.user.is_authenticated:
        messages.success(request, "Payment successful! Your order has been placed.")
        return redirect('dashboard:dashboard')  # Go to dashboard if logged in
    else:
        return render(request, "checkout/success.html")


def checkout_cancel(request):
    """Handles a cancelled payment."""
    return render(request, "checkout/cancel.html")


def send_order_email(order):
    """Sends an email confirmation for the order."""
    subject = f"Order #{order.id} Confirmation"
    message = render_to_string('checkout/order_confirmation_email.html', {'order': order})

    print(f"Sending order email to {order.email} with order items")
    for item in order.items.all():
        print(f" - {item.project.title} (Qty: {item.quantity}) - £{item.project.price}")

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],  # Send to the customer's email
        fail_silently=False,
        html_message=message,  # Include HTML content if available
    )
