from django.contrib import admin

from .models import (
    Superinvestor, 
    SuperinvestorActivity, 
    Period,
    SuperinvestorHistory
)


@admin.register(SuperinvestorHistory)
class SuperinvestorHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'superinvestor_related',
        'period_related',
        'company',
        'company_name',
        'portfolio_change',
        'movement',
        'shares',
        'reported_price',
        'portfolio_weight',
    ]


@admin.register(Superinvestor)
class SuperinvestorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'fund_name',
        'slug',
        'image',
        'last_update',
        'has_error',
    ]
    list_editable = [
        'image'
    ]


@admin.register(SuperinvestorActivity)
class SuperinvestorActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'superinvestor_related',
        'period_related',
        'company',
        'percentage_share_change',
        'share_change',
        'portfolio_change',
        'is_new',
        'movement',
        'company_name',
        'not_registered_company',
        'need_verify_company',

    ] 


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'year',
        'period',
    ]