from django.contrib import admin

from .models import (
    Customer,
    Product,
    ProductComment,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount,
    ProductComplementaryPaymentLink,
    StripeWebhookResponse
)



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
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductComplementaryInline]
    list_display = [
        'id',
        'title',
        'slug',
        'stripe_id',
        'visits',
        'is_active',
        'created_at',
        'updated_at'
    ]
    list_editable = ['is_active']
    list_filter = ['is_active']
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


@admin.action(description='Create payment link')
def create_payment_link(modeladmin, request, queryset):
    for query in queryset:
        ProductComplementaryPaymentLink.objects.create(
            product_complementary=query
        )


@admin.register(ProductComplementary)
class ProductComplementaryAdmin(admin.ModelAdmin):
    actions = [create_payment_link]
    inlines = [ProductComplementaryPaymentLinkInline]
    list_display = [
        'id',
        'title',
        'product',
        'price',
        'is_active',
        'payment_type',
        'stripe_id',
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

