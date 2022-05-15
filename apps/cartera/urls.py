from django.urls import path


from .api.urls import urlpatterns
from .views import (
    InicioCarteraView,
    InicioCashflowView,
    InicioPortfolioView
)

app_name = "cartera"
urlpatterns = [
    path('patrimoine-dashboard/', InicioCarteraView.as_view(), name='portfolio_inicio'),
    path('cartera-dashboard/', InicioPortfolioView.as_view(), name='cartera_inicio'),
    path('financials-dashboard/', InicioCashflowView.as_view(), name='financials_inicio'),
] + urlpatterns