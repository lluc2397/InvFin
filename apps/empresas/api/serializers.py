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
        exclude = ['id', 'year']


class IncomeStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:        
        model = IncomeStatement
        exclude = ['id', 'year']


class BalanceSheetSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:
        model = BalanceSheet
        exclude = ['id', 'year']


class CashflowStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    
    class Meta:
        model = CashflowStatement
        exclude = ['id', 'year']


class RentabilityRatioSerializer(ModelSerializer):

    class Meta:
        model = RentabilityRatio
        exclude = ['id', 'year']


class LiquidityRatioSerializer(ModelSerializer):

    class Meta:
        model = LiquidityRatio
        exclude = ['id', 'year']


class MarginRatioSerializer(ModelSerializer):

    class Meta:
        model = MarginRatio
        exclude = ['id', 'year']


class FreeCashFlowRatioSerializer(ModelSerializer):

    class Meta:
        model = FreeCashFlowRatio
        exclude = ['id', 'year']


class PerShareValueSerializer(ModelSerializer):

    class Meta:
        model = PerShareValue
        exclude = ['id', 'year']


class NonGaapSerializer(ModelSerializer):

    class Meta:
        model = NonGaap
        exclude = ['id', 'year']


class OperationRiskRatioSerializer(ModelSerializer):

    class Meta:
        model = OperationRiskRatio
        exclude = ['id', 'year']


class EnterpriseValueRatioSerializer(ModelSerializer):

    class Meta:
        model = EnterpriseValueRatio
        exclude = ['id', 'year']


class CompanyGrowthSerializer(ModelSerializer):

    class Meta:
        model = CompanyGrowth
        exclude = ['id', 'year']


class EficiencyRatioSerializer(ModelSerializer):

    class Meta:
        model = EficiencyRatio
        exclude = ['id', 'year']


class PriceToRatioSerializer(ModelSerializer):

    class Meta:
        model = PriceToRatio
        exclude = ['id', 'year']


