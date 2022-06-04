from django.db.models import signals

from apps.business.models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)
from apps.business.signals.handlers import BusinessSignal

signals.pre_delete.connect(BusinessSignal.product_pre_delete, sender=Product)
signals.pre_save.connect(BusinessSignal.product_pre_save, sender=Product)
signals.pre_save.connect(BusinessSignal.product_complementary_pre_save, sender=ProductComplementary)
signals.pre_save.connect(BusinessSignal.product_discount_pre_save, sender=ProductDiscount)