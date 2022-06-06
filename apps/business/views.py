from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from apps.seo.views import SEOListView, SEODetailView, SEOTemplateView

from .models import Product

import stripe
import json

stripe.api_key = settings.STRIPE_PRIVATE

STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC



class ProductsListView(SEOListView):
    model = Product
    meta_description = 'Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis.'
    meta_title = 'Las herramientas inteligentes para invertir como un experto'
    context_object_name = 'products'
    ordering = ['-visits']


class ProductDetailView(SEODetailView):
    model = Product

    def get(self, request, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        product.visits += 1
        product.save(update_fields=['visits'])
        return super().get(request, *args, **kwargs)


class CheckoutView(SEOTemplateView):
    meta_description = 'Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis.'
    meta_title = 'Caja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
