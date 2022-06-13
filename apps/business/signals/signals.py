from django.db.models import signals

from apps.business.models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount,
    ProductComplementaryPaymentLink
)
from apps.business.signals.handlers import BusinessSignal

signals.pre_save.connect(BusinessSignal.product_pre_save, sender=Product)
signals.pre_save.connect(BusinessSignal.product_complementary_pre_save, sender=ProductComplementary)
signals.pre_save.connect(BusinessSignal.complementary_payment_link_pre_save, sender=ProductComplementaryPaymentLink)
signals.pre_save.connect(BusinessSignal.product_discount_pre_save, sender=ProductDiscount)
signals.post_save.connect(BusinessSignal.transaction_post_save, sender=TransactionHistorial)