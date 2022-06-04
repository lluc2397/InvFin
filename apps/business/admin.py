from django.contrib import admin

from .models import (
    Customer,
    Product,
    ProductComment,
    TransactionHistorial,
    ProductComplementary,
    ProductDiscount
)


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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'slug',
        'stripe_id',
        'visits',
        'created_at',
        'updated_at'
    ]
    list_editable = []
    list_filter = []
    search_fields= []


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


@admin.register(ProductComplementary)
class ProductComplementaryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'secondary_title',
        'product',
        'price',
        'payment_type',
        'stripe_price_id',
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

