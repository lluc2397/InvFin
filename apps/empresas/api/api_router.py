from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.empresas.api.views import (
    IncomeStatementViewSet,
    BalanceSheetViewSet,
    CashflowStatementViewSet,
    RentabilityRatioViewSet,
    LiquidityRatioViewSet,
    MarginRatioViewSet,
    FreeCashFlowRatioViewSet,
    PerShareValueViewSet,
    NonGaapViewSet,
    OperationRiskRatioViewSet,
    EnterpriseValueRatioViewSet,
    CompanyGrowthViewSet,
    EficiencyRatioViewSet,
    PriceToRatioViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("IncomeStatement", IncomeStatementViewSet, basename="IncomeStatement")
router.register("BalanceSheet", BalanceSheetViewSet, basename="BalanceSheet")
router.register("CashflowStatement", CashflowStatementViewSet, basename="CashflowStatement")
router.register("RentabilityRatio", RentabilityRatioViewSet, basename="RentabilityRatio")
router.register("LiquidityRatio", LiquidityRatioViewSet, basename="LiquidityRatio")
router.register("MarginRatio", MarginRatioViewSet, basename="MarginRatio")
router.register("FreeCashFlowRatio", FreeCashFlowRatioViewSet, basename="FreeCashFlowRatio")
router.register("PerShareValue", PerShareValueViewSet, basename="PerShareValue")
router.register("NonGaap", NonGaapViewSet, basename="NonGaap")
router.register("OperationRiskRatio", OperationRiskRatioViewSet, basename="OperationRiskRatio")
router.register("EnterpriseValueRatio", EnterpriseValueRatioViewSet, basename="EnterpriseValueRatio")
router.register("CompanyGrowth", CompanyGrowthViewSet, basename="CompanyGrowth")
router.register("EficiencyRatio", EficiencyRatioViewSet, basename="EficiencyRatio")
router.register("PriceToRatio", PriceToRatioViewSet, basename="PriceToRatio")


urlpatterns = router.urls