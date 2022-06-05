from apps.business.models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)
from django.utils import timezone
from django.template.defaultfilters import slugify

from apps.business.stripe_management import StripeManagement
from apps.business import constants

class BusinessSignal:
    @classmethod
    def generate_content(cls, instance):
        prod = getattr(instance, 'product', None)

        if prod:
            description = prod.description
        else:
            description = instance.title
        
        if not instance.description:
            instance.description = description

        if not instance.slug:
            instance.slug = slugify(instance.title)
    
    @classmethod
    def product_pre_save(cls, sender, instance: Product, **kwargs):
        stripe = StripeManagement()
        if not instance.pk:
            BusinessSignal.generate_content(instance)
            stripe_product = stripe.create_product(instance.title, instance.description, instance.is_active)
            instance.stripe_id = stripe_product['id']
        else:
            stripe_product = stripe.update_product(
                instance.stripe_id, 
                instance.title, 
                instance.description, 
                instance.is_active
            )
        instance.updated_at = timezone.now()

    @classmethod
    def product_complementary_pre_save(cls, sender, instance: Product, **kwargs):
        stripe = StripeManagement()

        is_recurring = False
        subscription_period = None
        subscription_interval = None
        if instance.payment_type == constants.TYPE_SUBSCRIPTION:
            is_recurring = True
            subscription_period = instance.subscription_period
            subscription_interval = instance.subscription_interval
        if not instance.pk:
            BusinessSignal.generate_content(instance)
            stripe_product_complementary = stripe.create_product_complementary(
                instance.product.stripe_id,
                instance.price,
                instance.currency.currency,

                is_recurring,
                subscription_period,
                subscription_interval
            )
            instance.stripe_id = stripe_product_complementary['id']
        else:
            stripe_product_complementary = stripe.update_product_complementary(
                instance.stripe_id,
                instance.is_active
            )
        instance.updated_at = timezone.now()

    @classmethod
    def product_discount_pre_save(cls, sender, instance: Product, **kwargs):
        # stripe = StripeManagement()
        # if not instance.pk:
        #     stripe_product_discount = stripe.create_product(instance.title, instance.is_active)
        #     instance.stripe_id = stripe_product_discount['id']
        # else:
        #     stripe_product_discount
        pass
