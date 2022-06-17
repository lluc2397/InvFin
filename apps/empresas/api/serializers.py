from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer
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
        exclude = ['id', 'order']


class ExchangeSerializer(ModelSerializer):
    country = StringRelatedField(many=False)

    class Meta:
        model = Exchange
        exclude = ['id', 'main_org']


class BasicCompanySerializer(ModelSerializer):
    exchange = StringRelatedField(many=False)
    currency = StringRelatedField(many=False)
    industry = StringRelatedField(many=False)
    sector = StringRelatedField(many=False)
    country = StringRelatedField(many=False)

    class Meta:
        model = Company
        exclude = [
            'id',
            'is_adr',
            'is_fund',
            'is_etf',
            'no_incs',
            'no_bs',
            'no_cfs',
            'description_translated',
            'has_logo',
            'updated',
            'last_update',
            'date_updated',
            'has_error',
            'error_message',
            'remote_image_imagekit',
            'remote_image_cloudinary',
        ]


class CompanyStockPriceSerializer(ModelSerializer):

    class Meta:
        model = CompanyStockPrice
        exclude = ['id', 'year']


class IncomeStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    company = StringRelatedField(many=False)

    class Meta:        
        model = IncomeStatement
        exclude = ['id', 'year']


class BalanceSheetSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    company = StringRelatedField(many=False)

    class Meta:
        model = BalanceSheet
        exclude = ['id', 'year']


class CashflowStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    company = StringRelatedField(many=False)
    
    class Meta:
        model = CashflowStatement
        exclude = ['id', 'year']


class RentabilityRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = RentabilityRatio
        exclude = ['id', 'year']


class LiquidityRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = LiquidityRatio
        exclude = ['id', 'year']


class MarginRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = MarginRatio
        exclude = ['id', 'year']


class FreeCashFlowRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = FreeCashFlowRatio
        exclude = ['id', 'year']


class PerShareValueSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = PerShareValue
        exclude = ['id', 'year']


class NonGaapSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = NonGaap
        exclude = ['id', 'year']


class OperationRiskRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = OperationRiskRatio
        exclude = ['id', 'year']


class EnterpriseValueRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = EnterpriseValueRatio
        exclude = ['id', 'year']


class CompanyGrowthSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = CompanyGrowth
        exclude = ['id', 'year']


class EficiencyRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = EficiencyRatio
        exclude = ['id', 'year']


class PriceToRatioSerializer(ModelSerializer):
    company = StringRelatedField(many=False)

    class Meta:
        model = PriceToRatio
        exclude = ['id', 'year']


class CompanySerializer(BasicCompanySerializer):
    inc_statements = IncomeStatementSerializer(many=True)
    balance_sheets = BalanceSheetSerializer(many=True)
    cf_statements = CashflowStatementSerializer(many=True)
    rentability_ratios = RentabilityRatioSerializer(many=True)
    liquidity_ratios = LiquidityRatioSerializer(many=True)
    margins = MarginRatioSerializer(many=True)
    fcf_ratios = FreeCashFlowRatioSerializer(many=True)
    per_share_values = PerShareValueSerializer(many=True)
    non_gaap_figures = NonGaapSerializer(many=True)
    operation_risks_ratios = OperationRiskRatioSerializer(many=True)
    ev_ratios = EnterpriseValueRatioSerializer(many=True)
    growth_rates = CompanyGrowthSerializer(many=True)
    efficiency_ratios = EficiencyRatioSerializer(many=True)
    price_to_ratios = PriceToRatioSerializer(many=True)

    class Meta:
        model = Company
        exclude = [
            'id',
            'is_adr',
            'is_fund',
            'is_etf',
            'no_incs',
            'no_bs',
            'no_cfs',
            'description_translated',
            'has_logo',
            'updated',
            'last_update',
            'date_updated',
            'has_error',
            'error_message',
            'remote_image_imagekit',
            'remote_image_cloudinary',
        ]
