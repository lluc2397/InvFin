from django.urls import path

from .views import (
    InicioCarteraView,
    save_cashflow_movement
)

app_name = "cartera"
urlpatterns = [
    path('manage-portfolio/', InicioCarteraView.as_view(), name='portfolio_inicio'),
    path('new-cashflow-move/', save_cashflow_movement, name='save_cashflow_movement'),
]