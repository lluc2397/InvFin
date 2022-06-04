from django.forms import (
    ModelForm,
    ValidationError,
    ModelForm,
    Textarea,
)

from .models import (
    Customer,
    Product,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)


class BaseBusinessForm(ModelForm):
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class CustomerForm(BaseBusinessForm):
    class Meta:
        model = Customer
        exclude = ['id']


class ProductForm(BaseBusinessForm):
    class Meta:
        model = Product
        exclude = ['id']
    
    def full_clean(self):


class TransactionHistorialForm(BaseBusinessForm):
    class Meta:
        model = TransactionHistorial
        exclude = ['id']


class ProductComplementaryForm(BaseBusinessForm):
    class Meta:
        model = ProductComplementary
        exclude = ['id']


class ProductDiscountForm(BaseBusinessForm):
    class Meta:
        model = ProductDiscount
        exclude = ['id']

