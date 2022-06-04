import stripe
from django.conf import settings


STRIPE_PRIVATE = settings.STRIPE_PRIVATE
STRIPE_PUBLIC = settings.STRIPE_PUBLIC


class StripeManagement:
    def __init__(self) -> None:
        stripe.api_key = STRIPE_PUBLIC
        self.stripe_product = stripe.Product
        self.stripe_price = stripe.Price
        self.stripe_customer = stripe.Customer
    
    def create_product(self, name:str, active:bool = False) -> dict:
        product = self.stripe_product.create(
        name=name,
        active=active,
        )
        return product

    def update_product(self, id:str, name:str = None, active:bool = None) -> dict:
        product = self.stripe_product.modify("id", name="Updated Product", active=True)
        return product
    
    def delete_product(self) -> dict:
        product = self.stripe_product.delete('{{PRODUCT_ID}}')
        return product
    
    def create_product_complementary(self) -> dict:
        price = self.stripe_price.create(
        product='{{PRODUCT_ID}}',
        unit_amount=1000,
        currency="usd",
        recurring={"interval": "month"},
        )
        return price
    
    def create_customer(self) -> dict:
        customer = self.stripe_customer.list_payment_methods(
        "cus_xxxxxxxxxxxxx",
        type="card",
        )
        return customer
