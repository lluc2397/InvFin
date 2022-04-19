from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json

from django.http.response import HttpResponse
from django.db.models import Q

from .models import Company, IncomeStatement, BalanceSheet, CashflowStatement
from .api.serializers import IncomeStatementSerializer, BalanceSheetSerializer, CashflowStatementSerializer
key = 'olLKY2dEO1jgZ4FURM60o7B90NyF05'

def companies_searcher(request):
    query = request.GET.get("term", "")
    companies_availables = Company.objects.filter(Q(name__icontains=query) | Q(ticker__icontains=query),
    no_incs = False,
    no_bs = False,
    no_cfs = False,
        )[:5]
    
    results = [f'{company.name} ({company.ticker})' for company in companies_availables]
    
    data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)


class ExcelAPIIncome(APIView):
    def get(self, request, format=None):
        excel_token = request.GET['api_key'] 
        ticker = request.GET['ticker']

        if excel_token == key:
            the_company = Company.objects.get(ticker = ticker)
            income_stmnt = IncomeStatement.objects.filter(company = the_company)
            income_serializer = IncomeStatementSerializer(income_stmnt, many=True)
            return Response(income_serializer.data)
        else:
            content = {'asegúrate de haber escrito correctamente': 'tu clave secreta y el ticker de la empresa'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class ExcelAPIBalance(APIView):
    def get(self, request, format=None):
        excel_token = request.GET['api_key'] 
        ticker = request.GET['ticker']

        if excel_token == key:
            the_company = Company.objects.get(ticker = ticker)
            balancesheet_sttm = BalanceSheet.objects.filter(company = the_company)
            balance_serializer = BalanceSheetSerializer(balancesheet_sttm, many=True)
            return Response(balance_serializer.data)
        else:
            content = {'asegúrate de haber escrito correctamente': 'tu clave secreta y el ticker de la empresa'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)


class ExcelAPICashflow(APIView):
    def get(self, request, format=None):
        excel_token = request.GET['api_key'] 
        ticker = request.GET['ticker']

        if excel_token == key:
            the_company = Company.objects.get(ticker = ticker)
            cashflow_sttm = CashflowStatement.objects.filter(company = the_company)
            cashflow_serializer = CashflowStatementSerializer(cashflow_sttm, many=True)
            return Response(cashflow_serializer.data)
        else:
            content = {'asegúrate de haber escrito correctamente': 'tu clave secreta y el ticker de la empresa'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
