from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer,
    FloatField
)

from apps.empresas.models import (
    ExchangeOrganisation,
    Exchange,
    Company,
    CompanyStockPrice,
    IncomeStatement,
    BalanceSheet,
    CashflowStatement,
    RentabilityRatio,
    LiquidityRatio,
    MarginRatio,
    FreeCashFlowRatio,
    PerShareValue,
    NonGaap,
    OperationRiskRatio,
    EnterpriseValueRatio,
    CompanyGrowth,
    EficiencyRatio,
    PriceToRatio,
    )


class ExchangeOrganisationSerializer(ModelSerializer):

    class Meta:
        model = ExchangeOrganisation
        exclude = ['id']


class ExchangeSerializer(ModelSerializer):

    class Meta:
        model = Exchange
        exclude = ['id']


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        exclude = ['id']


class CompanyStockPriceSerializer(ModelSerializer):

    class Meta:
        model = CompanyStockPrice
        exclude = ['id']


class IncomeStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:        
        model = IncomeStatement
        exclude = ['id']


class BalanceSheetSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:
        model = BalanceSheet
        exclude = ['id']


class CashflowStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    
    class Meta:
        model = CashflowStatement
        exclude = ['id']


class RentabilityRatioSerializer(ModelSerializer):

    class Meta:
        model = RentabilityRatio
        exclude = ['id']


class LiquidityRatioSerializer(ModelSerializer):

    class Meta:
        model = LiquidityRatio
        exclude = ['id']


class MarginRatioSerializer(ModelSerializer):

    class Meta:
        model = MarginRatio
        exclude = ['id']


class FreeCashFlowRatioSerializer(ModelSerializer):

    class Meta:
        model = FreeCashFlowRatio
        exclude = ['id']


class PerShareValueSerializer(ModelSerializer):

    class Meta:
        model = PerShareValue
        exclude = ['id']


class NonGaapSerializer(ModelSerializer):

    class Meta:
        model = NonGaap
        exclude = ['id']


class OperationRiskRatioSerializer(ModelSerializer):

    class Meta:
        model = OperationRiskRatio
        exclude = ['id']


class EnterpriseValueRatioSerializer(ModelSerializer):

    class Meta:
        model = EnterpriseValueRatio
        exclude = ['id']


class CompanyGrowthSerializer(ModelSerializer):

    class Meta:
        model = CompanyGrowth
        exclude = ['id']


class EficiencyRatioSerializer(ModelSerializer):

    class Meta:
        model = EficiencyRatio
        exclude = ['id']


class PriceToRatioSerializer(ModelSerializer):

    class Meta:
        model = PriceToRatio
        exclude = ['id']


