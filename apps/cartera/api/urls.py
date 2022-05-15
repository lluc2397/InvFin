from django.urls import path

from .views import (
    AddCashflowMoveView,
    AddPositionMovementView,
    AddDefaultCurrencyView,
    AddNewAssetView,
    AddCategoriesView,
    AddFinancialObjectifView,
    
    
)


urlpatterns = [
    path('new-cashflow-move/', AddCashflowMoveView.as_view(), name='save_cashflow_movement'),
    path('new-asset-move/', AddPositionMovementView.as_view(), name='save_asset_movement'),
    path('edit-default-currency/', AddDefaultCurrencyView.as_view(), name='save_default_currency'),
    path('save-new-asset/', AddNewAssetView.as_view(), name='save_new_asset_movement'),
    path('save-new-category/', AddCategoriesView.as_view(), name='save_new_category'),
    path('save-new-objectif/', AddFinancialObjectifView.as_view(), name='save_new_objectif'),
]