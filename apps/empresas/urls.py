from django.urls import path

from .views import ExcelAPIBalance, ExcelAPICashflow, ExcelAPIIncome, companies_searcher

app_name = "empresas"
urlpatterns = [
    path('search-only-company', companies_searcher, name='searcher_companies'),

    path('company-information/excel-api/income', ExcelAPIIncome.as_view(), name='ExcelAPIIncome'),
    path('company-information/excel-api/balance', ExcelAPIBalance.as_view(), name='ExcelAPIBalance'),
    path('company-information/excel-api/cashflow', ExcelAPICashflow.as_view(), name='ExcelAPICashflow'),
]