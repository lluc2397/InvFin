from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify

from apps.api.models import Key
from apps.business.models import (
    Product,
    TransactionHistorial,
    ProductDiscount,
    ProductComplementaryPaymentLink,
    ProductSubscriber
)
from apps.business.stripe_management import StripeManagement
from apps.business import constants

from apps.users import constants as credits_constants
from apps.users.models import CreditUsageHistorial


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
    def complementary_payment_link_pre_save(cls, sender, instance: ProductComplementaryPaymentLink, **kwargs):
        stripe = StripeManagement()
        if not instance.pk and instance.for_website:
            payment_link = stripe.create_payment_link(instance)
            instance.link = payment_link['url']
            instance.stripe_id = payment_link['id']
    
    @classmethod
    def product_discount_pre_save(cls, sender, instance: ProductDiscount, **kwargs):
        stripe = StripeManagement()
    
    @classmethod
    def transaction_post_save(cls, sender, instance: TransactionHistorial, **kwargs):
        user = instance.customer.user
        if instance.product_complementary.purchase_result == constants.ADD_CREDITS:
            CreditUsageHistorial.objects.update_credits(
                user, 
                int(instance.product_complementary.product_result),
                credits_constants.ADD,
                credits_constants.BOUGHT_CREDITS, 
                instance.product_complementary
            )
        elif instance.product_complementary.purchase_result == constants.SHARE_EXCEL:
            pass
        #Create something to invite the user to purchase a subscription to get unlimited credits
        elif instance.product_complementary.purchase_result == constants.ILIMITED_CREDITS:
            subscription = ProductSubscriber.objects.create(
                product=instance.product,
                product_complementary=instance.product_complementary,
                subscriber=user
            )
            Key.objects.create(
                user=user,
                subscription=subscription
            )
