from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer,
    SerializerMethodField
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
    inc_statements = SerializerMethodField()
    balance_sheets = SerializerMethodField()
    cf_statements = SerializerMethodField()
    rentability_ratios = SerializerMethodField()
    liquidity_ratios = SerializerMethodField()
    margins = SerializerMethodField()
    fcf_ratios = SerializerMethodField()
    per_share_values = SerializerMethodField()
    non_gaap_figures = SerializerMethodField()
    operation_risks_ratios = SerializerMethodField()
    ev_ratios = SerializerMethodField()
    growth_rates = SerializerMethodField()
    efficiency_ratios = SerializerMethodField()
    price_to_ratios = SerializerMethodField()

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
    
    def slicing(self) -> int:
        return 10

    def get_inc_statements(self, obj):
        limit = self.slicing()
        queryset = obj.inc_statements.all()[:limit]
        return IncomeStatementSerializer(queryset, many=True).data


    def get_balance_sheets(self, obj):
        limit = self.slicing()
        queryset = obj.balance_sheets.all()[:limit]
        return BalanceSheetSerializer(queryset, many=True).data


    def get_cf_statements(self, obj):
        limit = self.slicing()
        queryset = obj.cf_statements.all()[:limit]
        return CashflowStatementSerializer(queryset, many=True).data


    def get_rentability_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.rentability_ratios.all()[:limit]
        return RentabilityRatioSerializer(queryset, many=True).data


    def get_liquidity_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.liquidity_ratios.all()[:limit]
        return LiquidityRatioSerializer(queryset, many=True).data


    def get_margins(self, obj):
        limit = self.slicing()
        queryset = obj.margins.all()[:limit]
        return MarginRatioSerializer(queryset, many=True).data


    def get_fcf_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.fcf_ratios.all()[:limit]
        return FreeCashFlowRatioSerializer(queryset, many=True).data


    def get_per_share_values(self, obj):
        limit = self.slicing()
        queryset = obj.per_share_values.all()[:limit]
        return PerShareValueSerializer(queryset, many=True).data


    def get_non_gaap_figures(self, obj):
        limit = self.slicing()
        queryset = obj.non_gaap_figures.all()[:limit]
        return NonGaapSerializer(queryset, many=True).data


    def get_operation_risks_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.operation_risks_ratios.all()[:limit]
        return OperationRiskRatioSerializer(queryset, many=True).data


    def get_ev_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.ev_ratios.all()[:limit]
        return EnterpriseValueRatioSerializer(queryset, many=True).data


    def get_growth_rates(self, obj):
        limit = self.slicing()
        queryset = obj.growth_rates.all()[:limit]
        return CompanyGrowthSerializer(queryset, many=True).data


    def get_efficiency_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.efficiency_ratios.all()[:limit]
        return EficiencyRatioSerializer(queryset, many=True).data


    def get_price_to_ratios(self, obj):
        limit = self.slicing()
        queryset = obj.price_to_ratios.all()[:limit]
        return PriceToRatioSerializer(queryset, many=True).data


