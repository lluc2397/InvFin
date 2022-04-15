from django.contrib import admin

from .models import (
    RoboAdvisorService,
    InvestorProfile,
    TemporaryInvestorProfile,
)


@admin.register(RoboAdvisorService)
class RoboAdvisorServiceAdmin(admin.ModelAdmin):
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

