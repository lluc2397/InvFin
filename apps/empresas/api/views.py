from django.contrib.auth import get_user_model

from apps.api.views import BaseAPIView
from apps.api.pagination import StandardResultPagination 

from apps.empresas.models import (
    Exchange
)
from apps.empresas.api.serializers import (
    ExchangeSerializer,
    CompanySerializer,
    BasicCompanySerializer,
    IncomeStatementSerializer,
    BalanceSheetSerializer,
    CashflowStatementSerializer
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
    custom_query = ()
    query_name = ['ticker']

    def get_object(self):
        ticker = self.request.query_params.get(self.query_name[0]).upper()
        return self.serializer_class.Meta.model.objects.prefetch_related(
            'inc_statements',
            'balance_sheets',
            'cf_statements',
            'rentability_ratios',
            'liquidity_ratios',
            'margins',
            'fcf_ratios',
            'per_share_values',
            'non_gaap_figures',
            'operation_risks_ratios',
            'ev_ratios',
            'growth_rates',
            'efficiency_ratios',
            'price_to_ratios'
        ).only(
            'ticker',
            'name',
            'sector',
            'website',
            'state',
            'country',
            'ceo',
            'image',
            'city',
            'employees',
            'address',
            'zip_code',
            'cik',
            'cusip',
            'isin',
            'description',
            'ipoDate',
        ).get(ticker=ticker), True


class CompanyIncomeStatementAPIView(BaseAPIView):
    serializer_class = IncomeStatementSerializer
    query_name = ['ticker']


class CompanyBalanceSheetAPIView(BaseAPIView):
    serializer_class = BalanceSheetSerializer
    query_name = ['ticker']


class CompanyCashflowStatementAPIView(BaseAPIView):
    serializer_class = CashflowStatementSerializer
    query_name = ['ticker']