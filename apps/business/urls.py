from django.urls import path

from .views import (
    CheckoutRedirectView,
    CreateCheckoutView,
    ProductDetailView,
    ProductsListView,
)
from .webhooks import stripe_webhook

app_name = "business"
urlpatterns = [
    path('las-mejores-herramientas-para-invertir', ProductsListView.as_view(), name='all_products'),
    path('la-mejor-herramienta-para-invertir-es/<slug>', ProductDetailView.as_view(), name='product'),

    path('create-checkout/<pk>/', CreateCheckoutView.as_view(), name='create_checkout'),
    path('pago-correcto/', CheckoutRedirectView.as_view(), name='order_success'),
    path('984dfgDFH68sDFg68s7fd', stripe_webhook, name='stripe_webhook'),
]