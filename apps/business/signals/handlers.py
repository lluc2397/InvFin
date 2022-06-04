from apps.business.models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)

from apps.business.stripe_management import StripeManagement

class BusinessSignal:
    
    @classmethod
    def product_pre_save(cls, sender, instance: Product):
        stripe = StripeManagement()
        if not instance.pk:
            stripe_product = stripe.create_product(instance.title, instance.is_active)
        else:
            stripe_product = stripe.update_product(instance.stripe_id, instance.title, instance.is_active)
        
        print(stripe_product)
        