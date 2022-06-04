import stripe
from django.conf import settings


STRIPE_PRIVATE = settings.STRIPE_PRIVATE
STRIPE_PUBLIC = settings.STRIPE_PUBLIC


stripe.api_key = STRIPE_PUBLIC

stripe.Product.create(
  name="Basic Dashboard",
  default_price_data={
    "unit_amount": 1000,
    "currency": "usd",
    "recurring": {"interval": "month"},
  },
  expand=["default_price"],
)

stripe.Product.modify("id", name="Updated Product", active=True)

stripe.Product.create(active=False, name="My product")

stripe.Product.delete('{{PRODUCT_ID}}')

stripe.Price.create(
  product='{{PRODUCT_ID}}',
  unit_amount=1000,
  currency="usd",
  recurring={"interval": "month"},
)

stripe.Customer.list_payment_methods(
  "cus_xxxxxxxxxxxxx",
  type="card",
)