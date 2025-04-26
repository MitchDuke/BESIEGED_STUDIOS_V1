import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'Invalid signature'}, status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # here, update your order model
        stripe_session_id = session.get['id']
        try:
            order = Order.objects.get(stripe_session_id=stripe_session_id)
            order.paid = True  # Assuming you have a paid field in your Order model
            order.save()

        except Order.DoesNotExist:
            pass  # Handle the case where the order does not exist

    return JsonResponse({'status': 'success'}, status=200)
