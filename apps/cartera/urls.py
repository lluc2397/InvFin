from django.urls import path

from .views import (
    InicioCarteraView,
    save_cashflow_movement,
    save_asset_movement,
    save_default_currency,
    save_new_asset_movement
)

app_name = "cartera"
urlpatterns = [
    path('manage-portfolio/', InicioCarteraView.as_view(), name='portfolio_inicio'),
    path('new-cashflow-move/', save_cashflow_movement, name='save_cashflow_movement'),
    path('new-asset-move/', save_asset_movement, name='save_asset_movement'),
    path('edit-default-currency/', save_default_currency, name='save_default_currency'),
    path('save-new-asset/', save_new_asset_movement, name='save_new_asset_movement'),
]