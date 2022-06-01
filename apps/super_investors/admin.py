from django.contrib import admin

from .models import Superinvestor, SuperinvestorActivity, Period


class SuperinvestorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'fund_name',
        'info_accronym',
        'slug',
        'last_update',
        'has_error',
    ]


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

    
class PeriodAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'year',
        'period',
    ]