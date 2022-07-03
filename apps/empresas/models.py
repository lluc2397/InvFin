from datetime import datetime

from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    JSONField,
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

from django.contrib.auth import get_user_model

from .managers import CompanyManager, CompanyUpdateLogManager
from apps.empresas.company.extension import CompanyExtended

User = get_user_model()


class ExchangeOrganisation(Model):
    name = CharField(max_length=250, null=True, blank=True)
    image = CharField(max_length=250, null=True, blank=True)
    sub_exchange1 = CharField(max_length=250, null=True, blank=True)
    sub_exchange2 = CharField(max_length=250, null=True, blank=True)
    order = PositiveIntegerField( null=True, blank=True)

    class Meta:
        verbose_name = "Organisation exchange"
        verbose_name_plural = "Organisation exchanges"
        db_table = "assets_exchanges_organisations"

    def __str__(self):
        return str(self.name)


class Exchange(Model):
    exchange_ticker = CharField(max_length=30, null=True, blank=True)
    exchange = CharField(max_length=250, null=True, blank=True)
    country = ForeignKey("general.Country", on_delete=SET_NULL, null=True, blank=True)
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
    DEFAULT_CHECKINGS = {
        'has_institutionals':{
            'state': 'no',
            'time': ''
        }
    }
    ticker = CharField(max_length=30, unique=True, db_index=True)
    name = CharField(max_length=700, null=True, blank=True)
    currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    industry = ForeignKey("general.Industry", on_delete=SET_NULL, null=True, blank=True)
    sector = ForeignKey("general.Sector", on_delete=SET_NULL, null=True, blank=True)
    website  = CharField(max_length=250 , null=True, blank=True)
    state = CharField(max_length=250 , null=True, blank=True)
    country =  ForeignKey("general.Country", on_delete=SET_NULL, null=True, blank=True)
    ceo = CharField(max_length=250 , null=True, blank=True)
    image = CharField(max_length=250 , null=True, blank=True)
    city  = CharField(max_length=250 , null=True, blank=True)
    employees = CharField(max_length=250 , null=True, blank=True)
    address = CharField(max_length=250 , null=True, blank=True)
    zip_code = CharField(max_length=250 , null=True, blank=True)
    cik = CharField(max_length=250 , null=True, blank=True)
    exchange = ForeignKey(Exchange, on_delete=SET_NULL, null=True, blank=True)
    cusip = CharField(max_length=250 , null=True, blank=True)
    isin = CharField(max_length=250 , null=True, blank=True)
    description = TextField( null=True, blank=True)
    ipoDate = CharField(max_length=250 , null=True, blank=True)
    beta = FloatField(default=0, blank=True, null=True)
    is_trust = BooleanField(default=False)
    last_div = FloatField(default=0, blank=True, null=True)
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
    has_error = BooleanField(default=False)
    error_message = TextField( null=True, blank=True)
    remote_image_imagekit = CharField(max_length=500 , default='', blank=True)
    remote_image_cloudinary = CharField(max_length=500 , default='', blank=True)
    checkings = JSONField(default=DEFAULT_CHECKINGS)

    objects = CompanyManager()

    class Meta:        
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        db_table = "assets_companies"
        ordering = ['ticker']
    
    def __str__(self):
        return str(self.ticker)
    
    def get_absolute_url(self):
        return reverse("screener:company", kwargs={"ticker": self.ticker})
    
    @property
    def full_name(self):
        return f'{self.ticker} {self.name}'
    
    @property
    def has_meta_image(self):
        if (
            'has_meta_image' in self.checkings and 
            self.check_checkings('has_meta_image')
        ):
            return True
        if self.remote_image_imagekit or self.remote_image_cloudinary:
            return True
        return False
    
    @property
    def meta_image(self):
        return self.remote_image_imagekit if self.remote_image_imagekit else self.remote_image_cloudinary
    
    @property
    def most_recent_year(self):
        return self.inc_statements.latest().date
    
    @property
    def short_introduction(self):
        current_ratios = self.calculate_current_ratios()
        last_income_statement = current_ratios['last_income_statement']
        currency = last_income_statement.reported_currency
        return (f"{self.ticker} ha tenido un crecimiento en sus ingresos del "
        f"{round(current_ratios['cagr'], 2)}% anualizado durante los últimos 10 años. "
        f"Actualmente la empresa genera {round(last_income_statement.revenue, 2)}{currency} "
        f"con gastos elevándose a {round(last_income_statement.cost_of_revenue, 2)}{currency}. "
        f"La empresa cotiza a {round(current_ratios['current_price'], 2)}{currency} por acción, con "
        f"{current_ratios['average_shares_out']} acciones en circulación la empresa obtiene una capitalización "
        f"bursátil de {round(current_ratios['marketcap'], 2)}{currency}")
    
    def check_checkings(self, main_dict: str):
        status = self.checkings[main_dict]['state']
        if status == 'no':
            return False
        return True
    
    def modify_checkings(self, main_dict: str, dict_state: str):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        self.checkings.update(
            {
                main_dict: 
                {
                    'state': dict_state,
                    'time': ts
                }
            }
        )
        self.save(update_fields=['checkings'])


class CompanyStockPrice(Model):
    company_related = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="stock_prices")
    date = IntegerField(default=0)
    year = DateTimeField(auto_now=True)
    price = FloatField(default=0, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Stock price"
        verbose_name_plural = "Stock prices"
        db_table = "assets_companies_stock_prices"

    def __str__(self):
        return str(self.company_related.ticker)


class CompanyUpdateLog(Model):
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="company_log_historial")
    date = DateTimeField(auto_now=True)
    where = CharField(max_length=250)
    had_error = BooleanField(default=False)
    error_message = TextField(default='', null=True)
    objects = CompanyUpdateLogManager()

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Logs"
        verbose_name_plural = "Logs"
        db_table = "assets_companies_updates_logs"

    def __str__(self):
        return str(self.company.ticker)


class IncomeStatement(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="inc_statements")
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    revenue = FloatField(default=0, blank=True, null=True)
    cost_of_revenue = FloatField(default=0, blank=True, null=True)
    gross_profit = FloatField(default=0, blank=True, null=True)
    rd_expenses = FloatField(default=0, blank=True, null=True)
    general_administrative_expenses = FloatField(default=0, blank=True, null=True)
    selling_marketing_expenses = FloatField(default=0, blank=True, null=True)
    sga_expenses = FloatField(default=0, blank=True, null=True)
    other_expenses = FloatField(default=0, blank=True, null=True)
    operating_expenses = FloatField(default=0, blank=True, null=True)
    cost_and_expenses = FloatField(default=0, blank=True, null=True)
    interest_expense = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    ebitda = FloatField(default=0, blank=True, null=True)
    operating_income = FloatField(default=0, blank=True, null=True)
    net_total_other_income_expenses = FloatField(default=0, blank=True, null=True)
    income_before_tax = FloatField(default=0, blank=True, null=True)
    income_tax_expenses = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)   
    weighted_average_shares_outstanding = FloatField(default=0, blank=True, null=True)
    weighted_average_diluated_shares_outstanding = FloatField(default=0, blank=True, null=True)

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
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    cash_and_cash_equivalents = FloatField(default=0, blank=True, null=True)
    short_term_investments = FloatField(default=0, blank=True, null=True)
    cash_and_short_term_investements = FloatField(default=0, blank=True, null=True)
    net_receivables = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    other_current_assets = FloatField(default=0, blank=True, null=True)
    total_current_assets = FloatField(default=0, blank=True, null=True)
    property_plant_equipement = FloatField(default=0, blank=True, null=True)
    goodwill = FloatField(default=0, blank=True, null=True)
    intangible_assets = FloatField(default=0, blank=True, null=True)
    goodwill_and_intangible_assets = FloatField(default=0, blank=True, null=True)
    long_term_investments = FloatField(default=0, blank=True, null=True)
    tax_assets = FloatField(default=0, blank=True, null=True)
    other_non_current_assets = FloatField(default=0, blank=True, null=True)
    total_non_current_assets = FloatField(default=0, blank=True, null=True)
    other_assets = FloatField(default=0, blank=True, null=True)
    total_assets = FloatField(default=0, blank=True, null=True)
    account_payables = FloatField(default=0, blank=True, null=True)
    shortTermDebt = FloatField(default=0, blank=True, null=True)
    taxPayables = FloatField(default=0, blank=True, null=True)
    deferredRevenue = FloatField(default=0, blank=True, null=True)
    other_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_current_liabilities = FloatField(default=0, blank=True, null=True)
    long_term_debt = FloatField(default=0, blank=True, null=True)
    deferred_revenue_non_current = FloatField(default=0, blank=True, null=True)
    deferred_tax_liabilities_non_current = FloatField(default=0, blank=True, null=True)
    other_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    other_liabilities = FloatField(default=0, blank=True, null=True)
    total_liabilities = FloatField(default=0, blank=True, null=True)
    common_stocks = FloatField(default=0, blank=True, null=True)
    retained_earnings = FloatField(default=0, blank=True, null=True)
    accumulated_other_comprehensive_income_loss = FloatField(default=0, blank=True, null=True)
    othertotal_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_liabilities_and_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_investments = FloatField(default=0, blank=True, null=True)
    total_debt = FloatField(default=0, blank=True, null=True)
    net_debt = FloatField(default=0, blank=True, null=True)
   
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
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    net_income = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    deferred_income_tax = FloatField(default=0, blank=True, null=True)
    stock_based_compesation = FloatField(default=0, blank=True, null=True)
    change_in_working_capital = FloatField(default=0, blank=True, null=True)
    accounts_receivables = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    accounts_payable = FloatField(default=0, blank=True, null=True)
    other_working_capital = FloatField(default=0, blank=True, null=True)
    other_non_cash_items = FloatField(default=0, blank=True, null=True)
    operating_activities_cf = FloatField(default=0, blank=True, null=True)
    investments_property_plant_equipment = FloatField(default=0, blank=True, null=True)
    acquisitions_net = FloatField(default=0, blank=True, null=True)
    purchases_investments = FloatField(default=0, blank=True, null=True)
    sales_maturities_investments = FloatField(default=0, blank=True, null=True)
    other_investing_activites = FloatField(default=0, blank=True, null=True)
    investing_activities_cf = FloatField(default=0, blank=True, null=True)
    debt_repayment = FloatField(default=0, blank=True, null=True)
    common_stock_issued = FloatField(default=0, blank=True, null=True)
    common_stock_repurchased = FloatField(default=0, blank=True, null=True)
    dividends_paid = FloatField(default=0, blank=True, null=True)
    other_financing_activities = FloatField(default=0, blank=True, null=True)
    financing_activities_cf = FloatField(default=0, blank=True, null=True)
    effect_forex_exchange = FloatField(default=0, blank=True, null=True)
    net_change_cash = FloatField(default=0, blank=True, null=True)
    cash_end_period = FloatField(default=0, blank=True, null=True)
    cash_beginning_period = FloatField(default=0, blank=True, null=True)
    operating_cf = FloatField(default=0, blank=True, null=True)
    capex = FloatField(default=0, blank=True, null=True)
    fcf = FloatField(default=0, blank=True, null=True)
    
    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Cash flow Statement"
        verbose_name_plural = "Cash flow Statements"
        db_table = "assets_companies_cashflow_statements"

    def __str__(self):
        return self.company.ticker + str(self.date)
    
    @property
    def cash_conversion_ratio(self):
        return self.fcf / self.net_income if self.net_income != 0 else 0

class RentabilityRatio(Model):
    date = IntegerField(default=0)
    year = DateField(auto_now=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="rentability_ratios")
    roa = FloatField(default=0, blank=True, null=True) 
    roe = FloatField(default=0, blank=True, null=True)
    roc = FloatField(default=0, blank=True, null=True)
    roce = FloatField(default=0, blank=True, null=True) 
    rota = FloatField(default=0, blank=True, null=True) 
    roic = FloatField(default=0, blank=True, null=True)
    nopatroic = FloatField(default=0, blank=True, null=True)
    rogic = FloatField(default=0, blank=True, null=True)

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
    cash_ratio = FloatField(default=0, blank=True, null=True)
    current_ratio = FloatField(default=0, blank=True, null=True)
    quick_ratio = FloatField(default=0, blank=True, null=True)
    operating_cashflow_ratio = FloatField(default=0, blank=True, null=True)
    debt_to_equity = FloatField(default=0, blank=True, null=True)

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
    gross_margin = FloatField(default=0, blank=True, null=True)
    ebitda_margin = FloatField(default=0, blank=True, null=True)
    net_income_margin = FloatField(default=0, blank=True, null=True)
    fcf_margin = FloatField(default=0, blank=True, null=True)
    fcf_equity_to_net_income = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_to_net_income = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_ebit_to_net_income = FloatField(default=0, blank=True, null=True)
    owners_earnings_to_net_income = FloatField(default=0, blank=True, null=True)

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
    fcf_equity = FloatField(default=0, blank=True, null=True)
    unlevered_fcf = FloatField(default=0, blank=True, null=True)
    unlevered_fcf_ebit = FloatField(default=0, blank=True, null=True)
    owners_earnings = FloatField(default=0, blank=True, null=True)

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
    sales_ps = FloatField(default=0, blank=True, null=True)
    book_ps = FloatField(default=0, blank=True, null=True)
    tangible_ps = FloatField(default=0, blank=True, null=True)
    fcf_ps = FloatField(default=0, blank=True, null=True)
    eps = FloatField(default=0, blank=True, null=True)
    cash_ps = FloatField(default=0, blank=True, null=True)
    operating_cf_ps = FloatField(default=0, blank=True, null=True)
    capex_ps = FloatField(default=0, blank=True, null=True)
    total_assets_ps = FloatField(default=0, blank=True, null=True)

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
    normalized_income = FloatField(default=0, blank=True, null=True)
    effective_tax_rate = FloatField(default=0, blank=True, null=True)    
    nopat = FloatField(default=0, blank=True, null=True)
    net_working_cap = FloatField(default=0, blank=True, null=True)
    average_inventory = FloatField(default=0, blank=True, null=True)
    average_payables = FloatField(default=0, blank=True, null=True)
    dividend_yield = FloatField(default=0, blank=True, null=True)
    earnings_yield = FloatField(default=0, blank=True, null=True)
    fcf_yield = FloatField(default=0, blank=True, null=True)
    income_quality = FloatField(default=0, blank=True, null=True)
    invested_capital = FloatField(default=0, blank=True, null=True)
    market_cap = FloatField(default=0, blank=True, null=True)
    net_current_asset_value = FloatField(default=0, blank=True, null=True)
    payout_ratio = FloatField(default=0, blank=True, null=True)
    tangible_assets = FloatField(default=0, blank=True, null=True)
    retention_ratio = FloatField(default=0, blank=True, null=True)

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
    asset_coverage_ratio = FloatField(default=0, blank=True, null=True)
    cashFlowCoverageRatios = FloatField(default=0, blank=True, null=True)
    cash_coverage = FloatField(default=0, blank=True, null=True)
    debt_service_coverage = FloatField(default=0, blank=True, null=True)
    interestCoverage = FloatField(default=0, blank=True, null=True)
    operating_cashflow_ratio = FloatField(default=0, blank=True, null=True)
    debtRatio = FloatField(default=0, blank=True, null=True)
    longTermDebtToCapitalization = FloatField(default=0, blank=True, null=True)
    totalDebtToCapitalization = FloatField(default=0, blank=True, null=True)

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
    market_cap = FloatField(default=0, blank=True, null=True)
    enterprise_value = FloatField(default=0, blank=True, null=True)
    ev_fcf = FloatField(default=0, blank=True, null=True)
    ev_operating_cf = FloatField(default=0, blank=True, null=True)
    ev_sales = FloatField(default=0, blank=True, null=True)
    company_equity_multiplier = FloatField(default=0, blank=True, null=True)
    ev_multiple = FloatField(default=0, blank=True, null=True)

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
    revenue_growth = FloatField(default=0, blank=True, null=True)
    cost_revenue_growth = FloatField(default=0, blank=True, null=True)
    operating_expenses_growth = FloatField(default=0, blank=True, null=True)
    net_income_growth = FloatField(default=0, blank=True, null=True)
    shares_buyback = FloatField(default=0, blank=True, null=True)
    eps_growth = FloatField(default=0, blank=True, null=True)
    fcf_growth = FloatField(default=0, blank=True, null=True)
    owners_earnings_growth = FloatField(default=0, blank=True, null=True)
    capex_growth = FloatField(default=0, blank=True, null=True)
    rd_expenses_growth = FloatField(default=0, blank=True, null=True)

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
    asset_turnover = FloatField(default=0, blank=True, null=True)
    inventory_turnover = FloatField(default=0, blank=True, null=True)
    fixed_asset_turnover = FloatField(default=0, blank=True, null=True)
    payables_turnover = FloatField(default=0, blank=True, null=True)
    cash_conversion_cycle = FloatField(default=0, blank=True, null=True)
    days_inventory_outstanding = FloatField(default=0, blank=True, null=True)
    days_payables_outstanding = FloatField(default=0, blank=True, null=True)
    days_sales_outstanding = FloatField(default=0, blank=True, null=True)
    fcf_to_operating_cf = FloatField(default=0, blank=True, null=True)
    operating_cycle = FloatField(default=0, blank=True, null=True)

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
    price_book = FloatField(default=0, blank=True, null=True)
    price_cf = FloatField(default=0, blank=True, null=True)
    price_earnings = FloatField(default=0, blank=True, null=True)
    price_earnings_growth = FloatField(default=0, blank=True, null=True)
    price_sales = FloatField(default=0, blank=True, null=True)
    price_total_assets = FloatField(default=0, blank=True, null=True)
    price_fcf = FloatField(default=0, blank=True, null=True)
    price_operating_cf = FloatField(default=0, blank=True, null=True)
    price_tangible_assets = FloatField(default=0, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Price to Ratio"
        verbose_name_plural = "Price to Ratios"
        db_table = "assets_companies_price_to_ratios"

    def __str__(self):
        return self.company.ticker + str(self.date)
    

class InstitutionalOrganization(Model):
    name = CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "Institutional Organization"
        verbose_name_plural = "Institutional Organizations"
        db_table = "assets_institutional_organizations"

    def __str__(self):
        return self.name


class TopInstitutionalOwnership(Model):
    date = IntegerField(default=0)
    year = DateField(blank=True, null=True)
    company = ForeignKey(
        Company, on_delete=SET_NULL, null=True, 
        blank=True, related_name="top_institutional_ownership"
    )
    organization = ForeignKey(
        InstitutionalOrganization, on_delete=SET_NULL, null=True, 
        blank=True, related_name="institution"
    )
    percentage_held = FloatField(default=0, blank=True, null=True)
    position = FloatField(default=0, blank=True, null=True)
    value = FloatField(default=0, blank=True, null=True)

    class Meta:
        get_latest_by = 'date'
        ordering = ['-date']
        verbose_name = "Top institutional owners"
        verbose_name_plural = "Top institutional owners"
        db_table = "assets_top_institutional_ownership"

    def __str__(self):
        return self.company.ticker + str(self.date)
