from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS
from rest_framework import status

from apps.empresas.api.serializers import (
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

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CompanyBaseAPIView(APIView):
    serializer_class = None
    permission_classes = [AllowAny|ReadOnly]

    def get(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)
        if status.is_success:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
