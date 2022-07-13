from django.contrib import admin
from django.forms import model_to_dict

from .models import (
    InvestorProfile,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorService,
    RoboAdvisorServiceStep,
    RoboAdvisorUserServiceActivity,
    RoboAdvisorUserServiceStepActivity,
    TemporaryInvestorProfile,
)


@admin.action(description='Create duplicate')
def create_duplicate(modeladmin, request, queryset):
    for query in queryset:
        kwargs = model_to_dict(query, exclude=['id', 'service_related'])
        RoboAdvisorServiceStep.objects.create(**kwargs)


@admin.register(RoboAdvisorServiceStep)
class RoboAdvisorServiceStepAdmin(admin.ModelAdmin):
    actions = [create_duplicate]

    list_display = [
        'id',
        'title',
        'order',
        'url',
        'template',
        'service_related'
    ]

    list_editable = [
        'template',
        'url',
        'order',
        'service_related'
    ]


class RoboAdvisorServiceStepInline(admin.StackedInline):
    model = RoboAdvisorServiceStep


@admin.register(RoboAdvisorService)
class RoboAdvisorServiceAdmin(admin.ModelAdmin):
    inlines = [RoboAdvisorServiceStepInline]

    list_display = [
        'id',
        'price',
        'order',
        'available',
        'title',
        'slug',
        'category',
        'template_result',
    ]

    list_editable = [
        'price',
        'order',
        'available',
        'title',
        'slug',
        'category',
        'template_result',
    ]


@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'updated_at',
        'created_at',
        'horizon',
        'risk_profile',
        'investor_type',
    ]


@admin.register(TemporaryInvestorProfile)
class TemporaryInvestorProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'profile_related',
        'created_at',
        'horizon',
        'risk_profile',
        'investor_type',
    ]


@admin.register(RoboAdvisorQuestionInvestorExperience)
class RoboAdvisorQuestionInvestorExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'age',
        'objectif',
        'investor_type_self_definition',
        'percentage_invested',
        'percentage_anualized_revenue',
        'time_investing_exp',
        'period_investing_exp',
    ]


@admin.register(RoboAdvisorQuestionCompanyAnalysis)
class RoboAdvisorQuestionCompanyAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'asset',
        'result',
        'sector_knowledge',
        'asset_knowledge',
        'amount_time_studied',
        'period_time_studied',
    ]


@admin.register(RoboAdvisorQuestionFinancialSituation)
class RoboAdvisorQuestionFinancialSituationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'average_income',
        'average_expense',
        'debt',
        'recurrent_savings',
        'recurrent_debts',
        'savings',
        'debt_percentage',
        'saving_percentage',
        'number_sources_income',
        'currency',
    ]


@admin.register(RoboAdvisorQuestionRiskAversion)
class RoboAdvisorQuestionRiskAversionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'volatilidad',
        'percentage_for_onefive',
        'percentage_for_three',
        'percentage_for_fourfive',
        'percentage_for_zerofive',
        'percentage_in_one_stock',
        'number_stocks',
    ]


@admin.register(RoboAdvisorQuestionPortfolioAssetsWeight)
class RoboAdvisorQuestionPortfolioAssetsWeightAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'etfs_percentage',
        'stocks_percentage',
        'bonds_percentage',
        'real_estate_percentage',
        'sofipos_percentage',
        'cryptos_percentage',
    ]


@admin.register(RoboAdvisorQuestionStocksPortfolio)
class RoboAdvisorQuestionStocksPortfolioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
    ]


@admin.register(RoboAdvisorQuestionPortfolioComposition)
class RoboAdvisorQuestionPortfolioCompositionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service_activity',
        'service_step',
        'asset',
        'sector_knowledge',
        'asset_knowledge',
        'amount_time_studied',
        'period_time_studied',
        'number_shares',
        'capital_invested',
        'sector_relationship',
    ]


@admin.register(RoboAdvisorUserServiceActivity)
class RoboAdvisorUserServiceActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'service',
        'date_started',
        'date_finished',
        'status',
    ]


@admin.register(RoboAdvisorUserServiceStepActivity)
class RoboAdvisorUserServiceStepActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'step',
        'date_started',
        'date_finished',
        'status',
    ]

