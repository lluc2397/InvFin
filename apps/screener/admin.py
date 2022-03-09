from django.contrib import admin

from .models import (
    FavoritesEtfsHistorial,
    FavoritesEtfsList,
    FavoritesStocksHistorial,
    FavoritesStocksList,
    UserCompanyObservation,
    UserScreenerMediumPrediction,
    UserScreenerSimplePrediction
)



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
