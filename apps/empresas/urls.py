from django.urls import path

from .views import (
    ExcelAPIIncome,
    ExcelAPIBalance,
    ExcelAPICashflow
)

app_name = "empresas"
urlpatterns = [
    path('company-information/excel-api/income', ExcelAPIIncome.as_view(), name='ExcelAPIIncome'),
    path('company-information/excel-api/balance', ExcelAPIBalance.as_view(), name='ExcelAPIBalance'),
    path('company-information/excel-api/cashflow', ExcelAPICashflow.as_view(), name='ExcelAPICashflow'),
]