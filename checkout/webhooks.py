import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # This is where the secret is used
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'status': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'status': 'Invalid signature'}, status=400)

    # Handle the session completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        stripe_session_id = session.get('id')

        try:
            order = Order.objects.get(stripe_session_id=stripe_session_id)
            order.paid = True  # assumes your model has a `paid` field
            order.save()
        except Order.DoesNotExist:
            pass  # Optional: Log this or raise a warning

    return JsonResponse({'status': 'success'}, status=200)