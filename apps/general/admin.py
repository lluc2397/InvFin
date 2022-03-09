from django.contrib import admin
from .models import (
    Category,
    Tag,
    Industry,
    Sector,
    Country,
    Currency
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name'
    ]


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'industry'
    ]


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'sector'
    ]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'currency'
    ]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'country'
    ]


