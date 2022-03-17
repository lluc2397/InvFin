from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    PositiveIntegerField,
    IntegerField,
    FloatField,
    DateField
)

from django.urls import reverse
from datetime import datetime

from apps.general.models import (
    Currency,
    Country,
    Industry,
    Sector
)

from .company_extension import CompanyExtended


class ExchangeOrganisation(Model):
    name = CharField(max_length=60000, null=True, blank=True)
    image = CharField(max_length=60000, null=True, blank=True)
    sub_exchange1 = CharField(max_length=60000, null=True, blank=True)
    sub_exchange2 = CharField(max_length=60000, null=True, blank=True)
    order = PositiveIntegerField( null=True, blank=True)

    class Meta:
        verbose_name = "Organisation exchange"
        verbose_name_plural = "Organisation exchanges"
        db_table = "assets_exchanges_organisations"

    def __str__(self):
        return str(self.name)


class Exchange(Model):
    exchange_ticker  = CharField(max_length=60000, null=True, blank=True)
    exchange  = CharField(max_length=60000, null=True, blank=True)
    country =  ForeignKey(Country, on_delete=SET_NULL, null=True, blank=True)
    main_org = ForeignKey(ExchangeOrganisation, on_delete=SET_NULL, null=True, blank=True)

    class Meta:        
        ordering = ['-exchange_ticker']
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"
        db_table = "assets_exchanges"

    def __str__(self):
        return str(self.exchange_ticker)

    @property
    def num_emps(self):
        return Company.objects.filter(exchange = self).count()


class Company(CompanyExtended):
    ticker = CharField(max_length=6000000)
    name = CharField(max_length=600000, null=True, blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    industry = ForeignKey(Industry, on_delete=SET_NULL, null=True, blank=True)
    sector = ForeignKey(Sector, on_delete=SET_NULL, null=True, blank=True)
    website  = CharField(max_length=6000000 , null=True, blank=True)
    state = CharField(max_length=6000000 , null=True, blank=True)
    country =  ForeignKey(Country, on_delete=SET_NULL, null=True, blank=True)
    ceo = CharField(max_length=6000000 , null=True, blank=True)
    image = CharField(max_length=6000000 , null=True, blank=True)
    city  = CharField(max_length=6000000 , null=True, blank=True)
    employees = CharField(max_length=6000000 , null=True, blank=True)
    address = CharField(max_length=6000000 , null=True, blank=True)
    zip_code = CharField(max_length=6000000 , null=True, blank=True)
    cik = CharField(max_length=6000000 , null=True, blank=True)
    exchange = ForeignKey(Exchange, on_delete=SET_NULL, null=True, blank=True)
    cusip = CharField(max_length=6000000 , null=True, blank=True)
    isin = CharField(max_length=6000000 , null=True, blank=True)
    description = TextField( null=True, blank=True)
    ipoDate = CharField(max_length=6000000 , null=True, blank=True)
    beta = FloatField(null=True, blank=True)
    is_trust = BooleanField(default=False)
    last_div = FloatField(null=True, blank=True)
    is_adr = BooleanField(default=False)
    is_fund = BooleanField(default=False)
    is_etf = BooleanField(default=False)
    no_incs = BooleanField(default=False)
    no_bs = BooleanField(default=False)
    no_cfs = BooleanField(default=False)
    description_translated = BooleanField(default=False)
    has_logo = BooleanField(default=False)
    updated = BooleanField(default=False)
    last_update = DateTimeField(null=True, blank=True)
    date_updated = BooleanField(default=False)

    class Meta:        
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "assets_companies"
        ordering = ['-name']
    
    def __str__(self):
        return str(self.ticker)
    
    def get_absolute_url(self):
        return reverse("screener:company", kwargs={"ticker": self.ticker})
    

    @property
    def most_recent_year(self):
        return self.inc_statements.latest().date


class CompanyStockPrice(Model):
    company_related = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="stock_prices")
    date = IntegerField(default=0)
    year = DateTimeField(auto_now=True)
    price = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Company stock price"
        verbose_name_plural = "Company stock prices"
        db_table = "assets_companies_stock_prices"

    def __str__(self):
        return str(self.company_related.ticker)


class IncomeStatement(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="inc_statements")
    reported_currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    revenue = FloatField(null=True, blank=True)
    cost_of_revenue = FloatField(null=True, blank=True)
    gross_profit = FloatField(null=True, blank=True)
    rd_expenses = FloatField(null=True, blank=True)
    general_administrative_expenses = FloatField(null=True, blank=True)
    selling_marketing_expenses = FloatField(null=True, blank=True)
    sga_expenses = FloatField(null=True, blank=True)
    other_expenses = FloatField(null=True, blank=True)
    operating_expenses = FloatField(null=True, blank=True)
    cost_and_expenses = FloatField(null=True, blank=True)
    interest_expense = FloatField(null=True, blank=True)
    depreciation_amortization = FloatField(null=True, blank=True)
    ebitda = FloatField(null=True, blank=True)
    operating_income = FloatField(null=True, blank=True)
    net_total_other_income_expenses = FloatField(null=True, blank=True)
    income_before_tax = FloatField(null=True, blank=True)
    income_tax_expenses = FloatField(null=True, blank=True)
    net_income = FloatField(null=True, blank=True)   
    weighted_average_shares_outstanding = FloatField(null=True, blank=True)
    weighted_average_diluated_shares_outstanding = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Income Statement"
        verbose_name_plural = "Income Statements"
        db_table = "assets_companies_income_statements"
    
    def __str__(self):
        return self.company.ticker + str(self.date)


class BalanceSheet(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="balance_sheets")
    reported_currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    cash_and_cash_equivalents = FloatField(null=True, blank=True)
    short_term_investments = FloatField(null=True, blank=True)
    cash_and_short_term_investements = FloatField(null=True, blank=True)
    net_receivables = FloatField(null=True, blank=True)
    inventory = FloatField(null=True, blank=True)
    other_current_assets = FloatField(null=True, blank=True)
    total_current_assets = FloatField(null=True, blank=True)
    property_plant_equipement = FloatField(null=True, blank=True)
    goodwill = FloatField(null=True, blank=True)
    intangible_assets = FloatField(null=True, blank=True)
    goodwill_and_intangible_assets = FloatField(null=True, blank=True)
    long_term_investments = FloatField(null=True, blank=True)
    tax_assets = FloatField(null=True, blank=True)
    other_non_current_assets = FloatField(null=True, blank=True)
    total_non_current_assets = FloatField(null=True, blank=True)
    other_assets = FloatField(null=True, blank=True)
    total_assets = FloatField(null=True, blank=True)
    account_payables = FloatField(null=True, blank=True)
    shortTermDebt = FloatField(null=True, blank=True)
    taxPayables = FloatField(null=True, blank=True)
    deferredRevenue = FloatField(null=True, blank=True)
    other_current_liabilities = FloatField(null=True, blank=True)
    total_current_liabilities = FloatField(null=True, blank=True)
    long_term_debt = FloatField(null=True, blank=True)
    deferred_revenue_non_current = FloatField(null=True, blank=True)
    deferred_tax_liabilities_non_current = FloatField(null=True, blank=True)
    other_non_current_liabilities = FloatField(null=True, blank=True)
    total_non_current_liabilities = FloatField(null=True, blank=True)
    other_liabilities = FloatField(null=True, blank=True)
    total_liabilities = FloatField(null=True, blank=True)
    common_stocks = FloatField(null=True, blank=True)
    retained_earnings = FloatField(null=True, blank=True)
    accumulated_other_comprehensive_income_loss = FloatField(null=True, blank=True)
    othertotal_stockholders_equity = FloatField(null=True, blank=True)
    total_stockholders_equity = FloatField(null=True, blank=True)
    total_liabilities_and_stockholders_equity = FloatField(null=True, blank=True)
    total_investments = FloatField(null=True, blank=True)
    total_debt = FloatField(null=True, blank=True)
    net_debt = FloatField(null=True, blank=True)
   
    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Balance Sheet"
        verbose_name_plural = "Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements"

    def __str__(self):
        return self.company.ticker + str(self.date)


class CashflowStatement(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="cf_statements")
    reported_currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    net_income = FloatField(null=True, blank=True)
    depreciation_amortization = FloatField(null=True, blank=True)
    deferred_income_tax = FloatField(null=True, blank=True)
    stock_based_compesation = FloatField(null=True, blank=True)
    change_in_working_capital = FloatField(null=True, blank=True)
    accounts_receivables = FloatField(null=True, blank=True)
    inventory = FloatField(null=True, blank=True)
    accounts_payable = FloatField(null=True, blank=True)
    other_working_capital = FloatField(null=True, blank=True)
    other_non_cash_items = FloatField(null=True, blank=True)
    operating_activities_cf = FloatField(null=True, blank=True)
    investments_property_plant_equipment = FloatField(null=True, blank=True)
    acquisitions_net = FloatField(null=True, blank=True)
    purchases_investments = FloatField(null=True, blank=True)
    sales_maturities_investments = FloatField(null=True, blank=True)
    other_investing_activites = FloatField(null=True, blank=True)
    investing_activities_cf = FloatField(null=True, blank=True)
    debt_repayment = FloatField(null=True, blank=True)
    common_stock_issued = FloatField(null=True, blank=True)
    common_stock_repurchased = FloatField(null=True, blank=True)
    dividends_paid = FloatField(null=True, blank=True)
    other_financing_activities = FloatField(null=True, blank=True)
    financing_activities_cf = FloatField(null=True, blank=True)
    effect_forex_exchange = FloatField(null=True, blank=True)
    net_change_cash = FloatField(null=True, blank=True)
    cash_end_period = FloatField(null=True, blank=True)
    cash_beginning_period = FloatField(null=True, blank=True)
    operating_cf = FloatField(null=True, blank=True)
    capex = FloatField(null=True, blank=True)
    fcf = FloatField(null=True, blank=True)
    
    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Cash flow Statement"
        verbose_name_plural = "Cash flow Statements"
        db_table = "assets_companies_cashflow_statements"

    def __str__(self):
        return self.company.ticker + str(self.date)

class RentabilityRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="rentability_ratios")
    roa = FloatField(null=True, blank=True) 
    roe = FloatField(null=True, blank=True)
    roc = FloatField(null=True, blank=True)
    roce = FloatField(null=True, blank=True) 
    rota = FloatField(null=True, blank=True) 
    roic = FloatField(null=True, blank=True)
    nopatroic = FloatField(null=True, blank=True)
    rogic = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Rentability Ratio"
        verbose_name_plural = "Rentability Ratios"
        db_table = "assets_companies_rentability_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)


class LiquidityRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="liquidity_ratios")
    cash_ratio = FloatField(null=True, blank=True)
    current_ratio = FloatField(null=True, blank=True)
    quick_ratio = FloatField(null=True, blank=True)
    operating_cashflow_ratio = FloatField(null=True, blank=True)
    debt_to_equity = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Liquidity Ratio"
        verbose_name_plural = "Liquidity Ratios"
        db_table = "assets_companies_liquidity_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)
    

class MarginRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="margins")
    gross_margin = FloatField(null=True, blank=True)
    ebitda_margin = FloatField(null=True, blank=True)
    net_income_margin = FloatField(null=True, blank=True)
    fcf_margin = FloatField(null=True, blank=True)
    fcf_equity_to_net_income = FloatField(null=True, blank=True)
    unlevered_fcf_to_net_income = FloatField(null=True, blank=True)
    unlevered_fcf_ebit_to_net_income = FloatField(null=True, blank=True)
    owners_earnings_to_net_income = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Margin Ratio"
        verbose_name_plural = "Margin Ratios"
        db_table = "assets_companies_margins_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)


class FreeCashFlowRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="fcf_ratios")
    fcf_equity = FloatField(null=True, blank=True)
    unlevered_fcf = FloatField(null=True, blank=True)
    unlevered_fcf_ebit = FloatField(null=True, blank=True)
    owners_earnings = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Free cash flow Ratio"
        verbose_name_plural = "Free cash flow Ratios"
        db_table = "assets_companies_freecashflow_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)


class PerShareValue(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="per_share_values")
    sales_ps = FloatField(null=True, blank=True)
    book_ps = FloatField(null=True, blank=True)
    tangible_ps = FloatField(null=True, blank=True)
    fcf_ps = FloatField(null=True, blank=True)
    eps = FloatField(null=True, blank=True)
    cash_ps = FloatField(null=True, blank=True)
    operating_cf_ps = FloatField(null=True, blank=True)
    capex_ps = FloatField(null=True, blank=True)
    total_assets_ps = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Per share"
        verbose_name_plural = "Per shares"
        db_table = "assets_companies_per_share_value"

    def __str__(self):
        return self.company.ticker + str(self.date)


class NonGaap(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="non_gaap_figures")
    normalized_income = FloatField(null=True, blank=True)
    effective_tax_rate = FloatField(null=True, blank=True)    
    nopat = FloatField(null=True, blank=True)
    net_working_cap = FloatField(null=True, blank=True)
    average_inventory = FloatField(null=True, blank=True)
    average_payables = FloatField(null=True, blank=True)
    dividend_yield = FloatField(null=True, blank=True)
    earnings_yield = FloatField(null=True, blank=True)
    fcf_yield = FloatField(null=True, blank=True)
    income_quality = FloatField(null=True, blank=True)
    invested_capital = FloatField(null=True, blank=True)
    market_cap = FloatField(null=True, blank=True)
    net_current_asset_value = FloatField(null=True, blank=True)
    payout_ratio = FloatField(null=True, blank=True)
    tangible_assets = FloatField(null=True, blank=True)
    retention_ratio = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Non GAAP figure"
        verbose_name_plural = "Non GAAP figures"
        db_table = "assets_companies_non_gaap"    

    def __str__(self):
        return  str(self.date)


class OperationRiskRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="operation_risks_ratios")
    asset_coverage_ratio = FloatField(null=True, blank=True)
    cashFlowCoverageRatios = FloatField(null=True, blank=True)
    cash_coverage = FloatField(null=True, blank=True)
    debt_service_coverage = FloatField(null=True, blank=True)
    interestCoverage = FloatField(null=True, blank=True)
    operating_cashflow_ratio = FloatField(null=True, blank=True)
    debtRatio = FloatField(null=True, blank=True)
    longTermDebtToCapitalization = FloatField(null=True, blank=True)
    totalDebtToCapitalization = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Operation Risk Ratio"
        verbose_name_plural = "Operation Risk Ratios"
        db_table = "assets_companies_operations_risk_ratio"    

    def __str__(self):
        return self.company.ticker + str(self.date)
    

class EnterpriseValueRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="ev_ratios")
    market_cap = FloatField(null=True, blank=True)
    enterprise_value = FloatField(null=True, blank=True)
    ev_fcf = FloatField(null=True, blank=True)
    ev_operating_cf = FloatField(null=True, blank=True)
    ev_sales = FloatField(null=True, blank=True)
    company_equity_multiplier = FloatField(null=True, blank=True)
    ev_multiple = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Enterprise Value"
        verbose_name_plural = "Enterprise Values"
        db_table = "assets_companies_enterprise_value_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)


class CompanyGrowth(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="growth_rates")
    revenue_growth = FloatField(null=True, blank=True)
    cost_revenue_growth = FloatField(null=True, blank=True)
    operating_expenses_growth = FloatField(null=True, blank=True)
    net_income_growth = FloatField(null=True, blank=True)
    shares_buyback = FloatField(null=True, blank=True)
    eps_growth = FloatField(null=True, blank=True)
    fcf_growth = FloatField(null=True, blank=True)
    owners_earnings_growth = FloatField(null=True, blank=True)
    capex_growth = FloatField(null=True, blank=True)
    rd_expenses_growth = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Company growth"
        verbose_name_plural = "Companies growth"
        db_table = "assets_companies_growths"

    def __str__(self):
        return self.company.ticker + str(self.date)


class EficiencyRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="efficiency_ratios")
    asset_turnover = FloatField(null=True, blank=True)
    inventory_turnover = FloatField(null=True, blank=True)
    fixed_asset_turnover = FloatField(null=True, blank=True)
    payables_turnover = FloatField(null=True, blank=True)
    cash_conversion_cycle = FloatField(null=True, blank=True)
    days_inventory_outstanding = FloatField(null=True, blank=True)
    days_payables_outstanding = FloatField(null=True, blank=True)
    days_sales_outstanding = FloatField(null=True, blank=True)
    fcf_to_operating_cf = FloatField(null=True, blank=True)
    operating_cycle = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Efficiency Ratio"
        verbose_name_plural = "Efficiency Ratios"
        db_table = "assets_companies_eficiency_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)


class PriceToRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True) 
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="price_to_ratios")
    price_book = FloatField(null=True, blank=True)
    price_cf = FloatField(null=True, blank=True)
    price_earnings = FloatField(null=True, blank=True)
    price_earnings_growth = FloatField(null=True, blank=True)
    price_sales = FloatField(null=True, blank=True)
    price_total_assets = FloatField(null=True, blank=True)
    price_fcf = FloatField(null=True, blank=True)
    price_operating_cf = FloatField(null=True, blank=True)
    price_tangible_assets = FloatField(null=True, blank=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Price to Ratio"
        verbose_name_plural = "Price to Ratios"
        db_table = "assets_companies_price_to_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)
    
    