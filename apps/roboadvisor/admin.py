from django.contrib import admin

from .models import (
    RoboAdvisorServiceStep,
    RoboAdvisorService,
    TemporaryInvestorProfile,
    InvestorProfile,

    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorQuestionPortfolioComposition,

    RoboAdvisorUserServiceActivity,
    RoboAdvisorUserServiceStepActivity
)

@admin.register(RoboAdvisorServiceStep)
class RoboAdvisorServiceStepAdmin(admin.ModelAdmin):
    list_display = [
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

# class RoboAdvisorServiceStepInline(admin.StackedInline):
#     model = RoboAdvisorServiceStep


@admin.register(RoboAdvisorService)
class RoboAdvisorServiceAdmin(admin.ModelAdmin):
    # inlines = [RoboAdvisorServiceStepInline]

    list_display = [
        'id',
        'price',
        'order',
        'available',
        'title',
        'description',
        'slug',
        'category'
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
        'id'
    ]


@admin.register(RoboAdvisorQuestionCompanyAnalysis)
class RoboAdvisorQuestionCompanyAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorQuestionFinancialSituation)
class RoboAdvisorQuestionFinancialSituationAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorQuestionRiskAversion)
class RoboAdvisorQuestionRiskAversionAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorQuestionPortfolioAssetsWeight)
class RoboAdvisorQuestionPortfolioAssetsWeightAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorQuestionStocksPortfolio)
class RoboAdvisorQuestionStocksPortfolioAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorQuestionPortfolioComposition)
class RoboAdvisorQuestionPortfolioCompositionAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorUserServiceActivity)
class RoboAdvisorUserServiceActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]


@admin.register(RoboAdvisorUserServiceStepActivity)
class RoboAdvisorUserServiceStepActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]

