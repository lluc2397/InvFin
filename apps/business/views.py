from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from django.views.generic import RedirectView
from django.contrib import messages
from django.contrib.auth import get_user_model

from apps.seo.views import SEOListView, SEODetailView, SEOTemplateView
from apps.general.models import Currency

from .models import (
    Product, 
    ProductComplementary, 
    TransactionHistorial,
    Customer
)

import stripe

User = get_user_model()
stripe.api_key = settings.STRIPE_PRIVATE
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC
FULL_DOMAIN = settings.FULL_DOMAIN
IS_TESTING = settings.DEBUG is True and settings.CURRENT_DOMAIN != settings.MAIN_DOMAIN


class ProductsListView(SEOListView):
    model = Product
    meta_description = 'Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis.'
    meta_title = 'Las herramientas inteligentes para invertir como un experto'
    context_object_name = 'products'
    ordering = ['-visits']

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, for_testing=IS_TESTING)


class ProductDetailView(SEODetailView):
    model = Product

    def get_object(self):
        return self.model._default_manager.get(
            slug=self.kwargs['slug'],
            is_active=True, 
            for_testing=IS_TESTING
            )

    def get(self, request, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        product.visits += 1
        product.save(update_fields=['visits'])
        return super().get(request, *args, **kwargs)


class CreateCheckoutView(SEODetailView):
    model = ProductComplementary
    meta_description = 'Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis.'
    meta_title = 'Caja'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        try:
            checkout_session = stripe.checkout.Session.create(  
                line_items=[{
                    'price': product.stripe_id,
                    'quantity': 1,
                }],
                payment_method_types=['card'],
                mode=product.payment_type,
                success_url= f'{FULL_DOMAIN}/pago-correcto/?prod={product.id}'+'&session_id={CHECKOUT_SESSION_ID}',
                cancel_url= f'{FULL_DOMAIN}/la-mejor-herramienta-para-invertir-es/{product.product.slug}',
            )
            
        except Exception as e:         
            return str(e)
        return redirect(checkout_session.url, code=303)


class CheckoutRedirectView(RedirectView):
    def save_transaction(self, stripe_response, customer, product_complementary):
        TransactionHistorial.objects.create(
            product=product_complementary.product,
            product_complementary=product_complementary,
            customer=customer,
            payment_method=stripe_response['payment_method_types'][0],
            currency=Currency.objects.get_or_create(currency=stripe_response['currency'].upper())[0],
            final_amount=(stripe_response['amount_total']/100),
            stripe_response=stripe_response
        )

    def get(self, request, *args, **kwargs):
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id'))
        product_complementary = ProductComplementary.objects.get(pk=request.GET.get('prod'))
        stripe_customer = stripe.Customer.retrieve(session.customer)
        user = User.objects.get_or_create_quick_user(self.request, stripe_customer['email'])
        customer, created = Customer.objects.get_or_create(user=user,defaults={'stripe_id': session.customer})
        self.save_transaction(session, customer, product_complementary)
        messages.success(request, 'Gracias por tu confianza.')
        url = reverse('users:user_inicio')
        return HttpResponseRedirect(url)


class CreateUserFromCustomerRecentPurchase(SEOTemplateView):
    template_name = 'business/post_purchase_waiting.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)