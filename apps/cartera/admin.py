from django.contrib import admin

from .models import (
    Asset,
    FinancialObjectif,
    Income,
    Patrimonio,
    PositionMovement,
    Spend,
)


@admin.register(PositionMovement)
class PositionMovementAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'move_type',
        'asset_related',
        'price',
        'date',
        'quantity',
        'currency',
        'fee',
    ]


@admin.register(Income)    
class IncomeAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
        'amount',
        'description',
        'date',
        'currency',
        'is_recurrent',
    ]


@admin.register(Spend)    
class SpendAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'name',
        'amount',
        'description',
        'date',
        'currency',
        'is_recurrent',
    ]


@admin.register(Asset)    
class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'object'
    ]


@admin.register(Patrimonio)    
class PatrimonioAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]


@admin.register(FinancialObjectif)
class FinancialObjectifAdmin(admin.ModelAdmin):
    list_display = [
        'user',

    ]