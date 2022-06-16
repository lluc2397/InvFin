from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ViewSet

from apps.empresas.api.serializers import (
    ExchangeSerializer,
    CompanySerializer,

    IncomeStatementSerializer,
    BalanceSheetSerializer,
    CashflowStatementSerializer,
    RentabilityRatioSerializer,
    LiquidityRatioSerializer,
    MarginRatioSerializer,
    FreeCashFlowRatioSerializer,
    PerShareValueSerializer,
    NonGaapSerializer,
    OperationRiskRatioSerializer,
    EnterpriseValueRatioSerializer,
    CompanyGrowthSerializer,
    EficiencyRatioSerializer,
    PriceToRatioSerializer)

User = get_user_model()

from django.apps import apps
from apps.api.views import BaseAPIView


class AllExchangesAPIView(BaseAPIView):
    serializer_class = ExchangeSerializer


class CompanySerializerAPIView(BaseAPIView):
    serializer_class = CompanySerializer


class CompanyBaseViewSet(ViewSet):

    def list(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class IncomeStatementViewSet(CompanyBaseViewSet):
    serializer_class = IncomeStatementSerializer


class BalanceSheetViewSet(CompanyBaseViewSet):
    serializer_class = BalanceSheetSerializer


class CashflowStatementViewSet(CompanyBaseViewSet):
    serializer_class = CashflowStatementSerializer


class RentabilityRatioViewSet(CompanyBaseViewSet):
    serializer_class = RentabilityRatioSerializer


class LiquidityRatioViewSet(CompanyBaseViewSet):
    serializer_class = LiquidityRatioSerializer


class MarginRatioViewSet(CompanyBaseViewSet):
    serializer_class = MarginRatioSerializer


class FreeCashFlowRatioViewSet(CompanyBaseViewSet):
    serializer_class = FreeCashFlowRatioSerializer


class PerShareValueViewSet(CompanyBaseViewSet):
    serializer_class = PerShareValueSerializer


class NonGaapViewSet(CompanyBaseViewSet):
    serializer_class = NonGaapSerializer


class OperationRiskRatioViewSet(CompanyBaseViewSet):
    serializer_class = OperationRiskRatioSerializer


class EnterpriseValueRatioViewSet(CompanyBaseViewSet):
    serializer_class = EnterpriseValueRatioSerializer


class CompanyGrowthViewSet(CompanyBaseViewSet):
    serializer_class = CompanyGrowthSerializer


class EficiencyRatioViewSet(CompanyBaseViewSet):
    serializer_class = EficiencyRatioSerializer


class PriceToRatioViewSet(CompanyBaseViewSet):
    serializer_class = PriceToRatioSerializer



