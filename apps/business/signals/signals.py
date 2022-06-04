from django.db.models import signals

from apps.business.models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)

from .handlers import BusinessSignal

signals.pre_save.connect(BusinessSignal.product_pre_save, sender=Product)