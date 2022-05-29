from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    OneToOneField,
    ForeignKey,
    SlugField,
    DateTimeField,
    BooleanField,
    IntegerField,
    ManyToManyField,
    JSONField,
    FloatField
)
from django.urls import reverse
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from apps.general.models import BaseComment

User = get_user_model()


class Customer(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True)
    created_at = DateTimeField(auto_now_add=True)
    stripe_id = CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        db_table = 'business_customers'

    def __str__(self):
        return self.user.username


class Product(Model):
    PRODUCT_TYPE = [
        ('subscription', 'Subscripción'),
        ('payment', 'Un pago')
    ]
    title = CharField(max_length=300, blank=True)
    slug = SlugField(max_length=300, null=True, blank=True)
    price = FloatField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    image = CharField(max_length=500, null=True, blank=True)
    video = CharField(max_length=500, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(null=True, blank=True)
    product_type = CharField(max_length=300, blank=True, choices=PRODUCT_TYPE)
    stripe_price_id = CharField(max_length=500, null=True, blank=True)
    visits = IntegerField(default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'business_products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Transaction_detail", kwargs={"pk": self.pk})


class ProductComment(BaseComment):
    rating = IntegerField(null=True, blank=True)
    content_related = ForeignKey(Product,
        on_delete=CASCADE,
        null=True,
        related_name = "comments_related")
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'business_products_comments'


class Transaction(Model):
    product = ForeignKey(Product, on_delete=SET_NULL, null=True)
    customer = ForeignKey(Customer, on_delete=SET_NULL, null=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = 'business_transactions'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Transaction_detail", kwargs={"pk": self.pk})
