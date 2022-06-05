import stripe
from django.conf import settings

from apps.general.models import Currency


STRIPE_PRIVATE = settings.STRIPE_PRIVATE
STRIPE_PUBLIC = settings.STRIPE_PUBLIC


class StripeManagement:
    def __init__(self) -> None:
        stripe.api_key = STRIPE_PRIVATE
        self.stripe_product = stripe.Product
        self.stripe_price = stripe.Price
        self.stripe_customer = stripe.Customer
    
    def create_product(self, name:str, description:str, active:bool = False) -> dict:
        product = self.stripe_product.create(
        name=name,
        description=description,
        active=active,
        )
        return product

    def update_product(self, stripe_id:str, name:str, description:str, active:bool) -> dict:
        product = self.stripe_product.modify(
            sid=stripe_id,
            name=name,
            description=description,
            active=active,
        )
        return product
    
    def disable_product(self, stripe_id:str) -> dict:
        product = self.stripe_product.modify(sid=stripe_id, active=False)
        return product
    
    def create_product_complementary(
        self,
        product_stripe_id:str,
        price:float,
        currency:str,
        is_recurring:bool = False,
        subscription_period:str = None,
        subscription_interval: int = None
    ) -> dict:

        price_data = {
            'product': product_stripe_id,
            'unit_amount': int(price*100),
            'currency': currency,
        }
        if is_recurring:
            price_data['recurring'] = {
                "interval": subscription_period,
                "interval_count": subscription_interval
            }
        
        price = self.stripe_price.create(**price_data)
        return price
    
    def update_product_complementary(
        self,
        stripe_price_id:str,
        active:bool = False,
    ) -> dict:

        price_data = {
            'sid': stripe_price_id,
            'active': active
        }

        price = self.stripe_price.modify(**price_data)
        return price
    
    def create_customer(
        self,
        currency:str,
        email:str,
        name:str
    ) -> dict:
        customer = self.stripe_customer.create(
            currency=currency,
            email=email,
            name=name
        )
        return customer
