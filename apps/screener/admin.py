from django.contrib import admin

from .models import (
    FavoritesEtfsHistorial,
    FavoritesEtfsList,
    FavoritesStocksHistorial,
    FavoritesStocksList,
    UserCompanyObservation,
    UserScreenerMediumPrediction,
    UserScreenerSimplePrediction,
    YahooScreener,
)


@admin.register(YahooScreener)
class YahooScreenerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
        'description',
        'yq_name',
        'asset_class_related',
        'show',
    ]
    list_editable = [
        'name',
        'slug',
        'asset_class_related',
        'show',
    ]



@admin.register(FavoritesEtfsHistorial)
class FavoritesEtfsHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(FavoritesEtfsList)
class FavoritesEtfsListAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(FavoritesStocksHistorial)
class FavoritesStocksHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(FavoritesStocksList)
class FavoritesStocksListAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(UserCompanyObservation)
class UserCompanyObservationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(UserScreenerMediumPrediction)
class UserScreenerMediumPredictionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]


@admin.register(UserScreenerSimplePrediction)
class UserScreenerSimplePredictionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
    ]
