from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()

import stripe

from .models import (
    StripeWebhookResponse, 
    ProductComplementary, 
    Product,
    Customer
)

stripe.api_key = settings.STRIPE_PRIVATE

STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC
EMAIL_DEFAULT = settings.EMAIL_DEFAULT

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    StripeWebhookResponse.objects.create(
        stripe_id=event['id'],
        full_response=event
        )
    if event["type"] == "payment_intent.created":
        event['data']['object']['receipt_email'] = stripe.Customer.retrieve(event['data']['object']["customer"])['email']

    # Handle the checkout.session.completed event
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # send_mail('Solicitud recibida',
		# f'{session}' ,
		# "contacto@inversionesyfinanzas.xyz",
		# ['a.inversionesyfinanzas@gmail.com'],)
    
    if event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
        customer_email = stripe_customer['email']

        user = User.objects.get_or_create_quick_user(request, customer_email)
        Customer.objects.get_or_create(user=user, stripe_id=stripe_customer_id)

        send_mail('Solicitud recibida',
		f'{intent}' ,
		EMAIL_DEFAULT,
		[EMAIL_DEFAULT],)

    
        
    return HttpResponse(status=200)