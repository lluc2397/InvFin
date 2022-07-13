import json

from django.db.models import Q
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .api.serializers import (
    BalanceSheetSerializer,
    CashflowStatementSerializer,
    IncomeStatementSerializer,
)
from .api.views import BaseAPIView
from .models import BalanceSheet, CashflowStatement, Company, IncomeStatement

key = 'olLKY2dEO1jgZ4FURM60o7B90NyF05'


def companies_searcher(request):
    query = request.GET.get("term", "")
    companies_availables = Company.objects.filter(Q(name__icontains=query) | Q(ticker__icontains=query),
    no_incs = False,
    no_bs = False,
    no_cfs = False,
        )[:10]
    
    results = [f'{company.name} [{company.ticker}]' for company in companies_availables]
    
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


class ExcelAPIIncome(BaseAPIView):
    custom_queryset = IncomeStatement
    serializer_class = IncomeStatementSerializer
    query_name = ['ticker']
    fk_lookup_model = 'company__ticker'


class ExcelAPIBalance(BaseAPIView):
    custom_queryset = BalanceSheet
    serializer_class = BalanceSheetSerializer
    query_name = ['ticker']
    fk_lookup_model = 'company__ticker'


class ExcelAPICashflow(BaseAPIView):
    custom_queryset = CashflowStatement
    serializer_class = CashflowStatementSerializer
    query_name = ['ticker']
    fk_lookup_model = 'company__ticker'
    