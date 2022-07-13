from django.contrib.auth import get_user_model

from apps.api.pagination import StandardResultPagination
from apps.api.views import BaseAPIView
from apps.empresas.api.serializers import (
    BalanceSheetSerializer,
    BasicCompanySerializer,
    CashflowStatementSerializer,
    CompanySerializer,
    ExchangeSerializer,
    IncomeStatementSerializer,
)
from apps.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    Company,
    Exchange,
    IncomeStatement,
)

User = get_user_model()


class AllExchangesAPIView(BaseAPIView):
    serializer_class = ExchangeSerializer
    queryset = Exchange
    pagination_class = StandardResultPagination


class BasicCompanyAPIView(BaseAPIView):
    serializer_class = BasicCompanySerializer
    query_name = ['ticker']


class CompleteCompanyAPIView(BaseAPIView):
    serializer_class = CompanySerializer
    custom_query = (Company.objects.fast_full(), False)
    query_name = ['ticker']


class CompanyIncomeStatementAPIView(BaseAPIView):
    serializer_class = IncomeStatementSerializer
    limited = True
    query_name = ['ticker']
    custom_queryset = IncomeStatement
    fk_lookup_model = 'company__ticker'


class CompanyBalanceSheetAPIView(BaseAPIView):
    serializer_class = BalanceSheetSerializer
    limited = True
    custom_queryset = BalanceSheet
    query_name = ['ticker']
    fk_lookup_model = 'company__ticker'


class CompanyCashflowStatementAPIView(BaseAPIView):
    serializer_class = CashflowStatementSerializer
    limited = True
    custom_queryset = CashflowStatement
    query_name = ['ticker']
    fk_lookup_model = 'company__ticker'