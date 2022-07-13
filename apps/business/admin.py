from django.contrib import admin

from .models import (
    Customer,
    Product,
    ProductComment,
    ProductComplementary,
    ProductComplementaryPaymentLink,
    ProductDiscount,
    StripeWebhookResponse,
    TransactionHistorial,
)


class BaseStripeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'stripe_id',
        'is_active',
        'for_testing',
        'created_at',
        'updated_at'
    ]
    list_editable = ['for_testing', 'is_active']
    list_filter = ['for_testing', 'is_active']
    search_fields= ['title']


@admin.register(StripeWebhookResponse)
class StripeWebhookResponseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'product_complementary',
        'customer',
        'created_at',
    ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'created_at',
        'stripe_id',
    ]
    list_editable = []
    list_filter = []
    search_fields = ['user__username']


class ProductComplementaryInline(admin.StackedInline):
    model = ProductComplementary


@admin.register(Product)
class ProductAdmin(BaseStripeAdmin):
    inlines = [ProductComplementaryInline]
    list_display = BaseStripeAdmin.list_display +[
        'slug',
        'visits',
    ]
    list_editable = ['for_testing', 'is_active']
    list_filter = ['for_testing', 'is_active']
    search_fields= ['title']


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'rating',
        'content_related',
        'created_at'
        
    ]
    list_editable = []
    list_filter = []
    search_fields= []


@admin.register(TransactionHistorial)
class TransactionHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product',
        'product_complementary',
        'product_comment',
        'customer',
        'created_at',
        'payment_method',
        'currency',
        'discount',
        'final_amount',
    ]
    list_editable = []
    list_filter = []
    search_fields= []


class ProductComplementaryPaymentLinkInline(admin.StackedInline):
    model = ProductComplementaryPaymentLink


@admin.action(description='Save testing copy')
def create_copy_testing(modeladmin, request, queryset):
    historial = {
        'old_id': None,
        'new_id': None,
    }
    for query in queryset.values():
        query.pop('id')
        product_id = query.pop('product_id')
        query.pop('stripe_id')
        if product_id != historial['old_id']:
            historial['old_id'] = product_id
            product = Product.objects.filter(id=product_id).values()[0]
            product.pop('id')
            product.pop('stripe_id')
            product['for_testing'] = True
            new_product = Product.objects.create(**product)
            historial['new_id'] = new_product.id
        query['product_id'] = historial['new_id']
        query['for_testing'] = True
        queryset.model.objects.create(**query)


@admin.action(description='Create payment link')
def create_payment_link(modeladmin, request, queryset):
    for query in queryset:
        ProductComplementaryPaymentLink.objects.create(
            product_complementary=query
        )


@admin.register(ProductComplementary)
class ProductComplementaryAdmin(BaseStripeAdmin):
    actions =  [create_copy_testing, create_payment_link]
    inlines = [ProductComplementaryPaymentLinkInline]
    list_display = BaseStripeAdmin.list_display + [
        'product',
        'price',
        'payment_type',
        'currency',
    ]
    list_editable = []
    list_filter = []
    search_fields= []


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display =[
        'id',
        'product',
        'product_complementary',
        'start_date',
        'end_date',
        'discount',
    ] 
    list_editable = []
    list_filter = []
    search_fields= []

