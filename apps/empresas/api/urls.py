from django.urls import path

from .views import (
    AllExchangesAPIView,
    CompleteCompanyAPIView,
    BasicCompanyAPIView,
    CompanyIncomeStatementAPIView,
    CompanyBalanceSheetAPIView,
    CompanyCashflowStatementAPIView
)

urlpatterns = [
    
    path('lista-exchanges/', AllExchangesAPIView.as_view()),
    path('empresa-completa/', CompleteCompanyAPIView.as_view()),
    path('empresa-basico/', BasicCompanyAPIView.as_view()),
    path('estado-resultados/', CompanyIncomeStatementAPIView.as_view()),
    path('balance-general/', CompanyBalanceSheetAPIView.as_view()),
    path('estado-flujo-efectivo/', CompanyCashflowStatementAPIView.as_view()),
]