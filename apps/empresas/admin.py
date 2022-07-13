from datetime import datetime

from django.conf import settings
from django.contrib import admin

from .company.update import UpdateCompany
from .models import (
    BalanceSheet,
    CashflowStatement,
    Company,
    CompanyGrowth,
    CompanyStockPrice,
    CompanyUpdateLog,
    EficiencyRatio,
    EnterpriseValueRatio,
    Exchange,
    ExchangeOrganisation,
    FreeCashFlowRatio,
    IncomeStatement,
    InstitutionalOrganization,
    LiquidityRatio,
    MarginRatio,
    NonGaap,
    OperationRiskRatio,
    PerShareValue,
    PriceToRatio,
    RentabilityRatio,
    TopInstitutionalOwnership,
)

IMAGEKIT_URL_ENDPOINT = settings.IMAGEKIT_URL_ENDPOINT
IMAGE_KIT = settings.IMAGE_KIT


@admin.register(CompanyUpdateLog)
class CompanyUpdateLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date',
        'where',
        'had_error',
        'error_message'
    ]
    search_fields = ['company__name']


@admin.register(InstitutionalOrganization)
class InstitutionalOrganizationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]
    search_fields = ['name']


@admin.register(TopInstitutionalOwnership)
class TopInstitutionalOwnershipAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'date',
        'year',
        'company',
        'organization',
        'percentage_held',
        'position',
        'value',
    ]
    


@admin.register(CashflowStatement)
class CashflowStatementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(IncomeStatement)
class IncomeStatementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.action(description='Save remote images')
def save_remote_imagekit(modeladmin, request, queryset):
    for query in queryset:
        if query.has_logo is False or query.remote_image_imagekit:
            continue
        imagekit_url = IMAGE_KIT.upload_file(
            file= query.image, # required
            file_name= f"{query.ticker}.webp", # required
            options= {
                "folder" : f"/companies/{query.sector.sector}/",
               "tags": [
                   query.ticker, query.exchange.exchange, 
                   query.country.country, query.sector.sector, 
                   query.industry.industry
                ],
                "is_private_file": False,
                "use_unique_file_name": False,
            }
        )
        image = imagekit_url['response']['url']
        imagekit_url = IMAGE_KIT.url({
            "src": image,
            "transformation": [{"height": "300", "width": "300"}],
        })
        query.remote_image_imagekit = imagekit_url
        query.save(update_fields=['remote_image_imagekit'])


@admin.action(description='Do a genreal update')
def do_general_update(modeladmin, request, queryset):
    for query in queryset:
        UpdateCompany(query).general_update()


@admin.action(description='Set has logo correctly')
def update_has_logo(modeladmin, request, queryset):
    for query in queryset:
        if not query.image:
            query.has_logo = False
            query.save(update_fields=['has_logo'])


@admin.action(description='Add new checking')
def update_has_logo(modeladmin, request, queryset):
    for query in queryset:
        state = 'no'
        if query.remote_image_imagekit or query.remote_image_cloudinary:
            state = 'yes'
        query.modify_checkings('has_meta_image', state)
        

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    actions = [save_remote_imagekit, update_has_logo, do_general_update]
    list_display = [
        'id',
        'name',
        'last_update',
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]
    list_filter = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'updated',
        'description_translated',
        'has_logo',
        'has_error',
        'exchange__main_org'
    ]
    list_editable = [
        'no_incs',
        'no_bs',
        'no_cfs',
        'description_translated',
        'has_logo',
    ]
    search_fields = ['name', 'ticker']

    
      

@admin.register(CompanyGrowth)
class CompanyGrowthAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(EficiencyRatio)
class EficiencyRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(EnterpriseValueRatio)
class EnterpriseValueRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'exchange_ticker',
        'exchange',
        'country',
        'main_org'
    ]
    search_fields = ['main_org_name']


@admin.register(ExchangeOrganisation)
class ExchangeOrganisationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'image',
        'sub_exchange1',
        'sub_exchange2',
        'order',
    ]
    list_editable = ['order']
    search_fields = ['name']


@admin.register(RentabilityRatio)
class RentabilityRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(MarginRatio)
class MarginRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(PriceToRatio)
class PriceToRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(LiquidityRatio)
class LiquidityRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(OperationRiskRatio)
class OperationRiskRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(FreeCashFlowRatio)
class FreeCashFlowRatioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(PerShareValue)
class PerShareValueAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']


@admin.register(CompanyStockPrice)
class CompanyStockPriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company_related',
        'date'
    ]
    search_fields = ['company_related_name']


@admin.register(NonGaap)
class NonGaapAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company',
        'date'
    ]
    search_fields = ['company_name', 'company_ticker']

