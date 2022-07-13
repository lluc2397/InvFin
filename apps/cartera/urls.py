from django.urls import path

from .api.urls import urlpatterns
from .views import (
    InicioCarteraView,
    InicioCashflowView,
    InicioPortfolioView,
    return_balance_table,
)

app_name = "cartera"
urlpatterns = [
    path('patrimoine-dashboard/', InicioCarteraView.as_view(), name='portfolio_inicio'),
    path('cartera-dashboard/', InicioPortfolioView.as_view(), name='cartera_inicio'),
    path('financials-dashboard/', InicioCashflowView.as_view(), name='financials_inicio'),

    path('retreive-own-balance-sheet/', return_balance_table, name='return_balance_table'),
] + urlpatterns