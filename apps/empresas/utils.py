from apps.general.models import Currency
from apps.translate.google_trans_new import google_translator

from .company_calculations import CompanyFinancials

from datetime import datetime

class UpdateCompany(CompanyFinancials):
    def __init__(self, company) -> None:
        self.company = company
        super().__init__()

    def add_logo(self):        
        try:
            self.company.image = self.yho_company.info['logo_url']
            self.company.has_logo = True
            self.company.save()
        except Exception as e:
            print(e)

    def add_description(self):
        try:
            self.company.description = google_translator().translate(self.company.description,lang_src='en', lang_tgt='es')
            self.company.description_translated = True
            self.company.save()
        except Exception as e:
            print(e)

    def general_update(self):        
        if self.company.has_logo is False:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()

    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()['asOfDate'].max().value // 10**9 # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year

        if least_recent_year != self.company.most_recent_year:
            return 'need update'
        return 'updated'
    
    def generate_current_data(self, data:dict):
        current_price = self.get_most_recent_price()
        data.update(current_price)
        return data
    
    def generate_last_year_data(self, data:dict):
        self.last_year_data(**data)

    def create_income_statement(self, inc_stt:dict):
        income_statement = self.company.inc_statements.create(
            date = inc_stt['calendarYear'],
            year = inc_stt['date'],
            reported_currency = Currency.objects.get_or_create(currency=inc_stt['reportedCurrency'])[0],
            revenue = inc_stt['revenue'],
            cost_of_revenue = inc_stt['costOfRevenue'],
            gross_profit = inc_stt['grossProfit'],
            rd_expenses = inc_stt['researchAndDevelopmentExpenses'],
            general_administrative_expenses = inc_stt['generalAndAdministrativeExpenses'],
            selling_marketing_expenses = inc_stt['sellingAndMarketingExpenses'],
            sga_expenses = inc_stt['sellingGeneralAndAdministrativeExpenses'],
            other_expenses = inc_stt['otherExpenses'],
            operating_expenses = inc_stt['operatingExpenses'],
            cost_and_expenses = inc_stt['costAndExpenses'],
            interest_expense = inc_stt['interestExpense'],
            depreciation_amortization = inc_stt['depreciationAndAmortization'],
            ebitda = inc_stt['ebitda'],
            operating_income = inc_stt['operatingIncome'],
            net_total_other_income_expenses = inc_stt['totalOtherIncomeExpensesNet'],
            income_before_tax = inc_stt['incomeBeforeTax'],
            income_tax_expenses = inc_stt['incomeTaxExpense'],
            net_income = inc_stt['netIncome'],
            weighted_average_shares_outstanding = inc_stt['weightedAverageShsOut'],
            weighted_average_diluated_shares_outstanding = inc_stt['weightedAverageShsOutDil'],)
        
        return income_statement
    
    def create_balance_sheet(self, bal_sht:dict):
        balance_sheet = self.company.balance_sheets.create(
            date = bal_sht['calendarYear'],
            year = bal_sht['date'],
            reported_currency = Currency.objects.get_or_create(currency=bal_sht['reportedCurrency'])[0],
            cash_and_cash_equivalents = bal_sht['cashAndCashEquivalents'],
            short_term_investments = bal_sht['shortTermInvestments'],
            cash_and_short_term_investements = bal_sht['cashAndShortTermInvestments'],
            net_receivables = bal_sht['netReceivables'],
            inventory = bal_sht['inventory'],
            other_current_assets = bal_sht['otherCurrentAssets'],
            total_current_assets = bal_sht['totalCurrentAssets'],
            property_plant_equipement = bal_sht['propertyPlantEquipmentNet'],
            goodwill = bal_sht['goodwill'],
            intangible_assets = bal_sht['intangibleAssets'],
            goodwill_and_intangible_assets = bal_sht['goodwillAndIntangibleAssets'],
            long_term_investments = bal_sht['longTermInvestments'],
            tax_assets = bal_sht['taxAssets'],
            other_non_current_assets = bal_sht['otherNonCurrentAssets'],
            total_non_current_assets = bal_sht['totalNonCurrentAssets'],
            other_assets = bal_sht['otherAssets'],
            total_assets = bal_sht['totalAssets'],
            account_payables = bal_sht['accountPayables'],
            shortTermDebt = bal_sht['shortTermDebt'],
            taxPayables = bal_sht['taxPayables'],
            deferredRevenue = bal_sht['deferredRevenue'],
            other_current_liabilities = bal_sht['otherCurrentLiabilities'],
            total_current_liabilities = bal_sht['totalCurrentLiabilities'],
            long_term_debt = bal_sht['longTermDebt'],
            deferred_revenue_non_current = bal_sht['deferredRevenueNonCurrent'],
            deferred_tax_liabilities_non_current = bal_sht['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities = bal_sht['otherNonCurrentLiabilities'],
            total_non_current_liabilities = bal_sht['totalNonCurrentLiabilities'],
            other_liabilities = bal_sht['otherLiabilities'],
            total_liabilities = bal_sht['totalLiabilities'],
            common_stocks = bal_sht['commonStock'],
            retained_earnings = bal_sht['retainedEarnings'],
            accumulated_other_comprehensive_income_loss = bal_sht['accumulatedOtherComprehensiveIncomeLoss'],
            othertotal_stockholders_equity = bal_sht['othertotalStockholdersEquity'],
            total_stockholders_equity = bal_sht['totalStockholdersEquity'],
            total_liabilities_and_stockholders_equity = bal_sht['totalLiabilitiesAndStockholdersEquity'],
            total_investments = bal_sht['totalInvestments'],
            total_debt = bal_sht['totalDebt'],
            net_debt = bal_sht['netDebt'],)
        
        return balance_sheet
    
    def create_cashflow_statement(self, csf_stt:dict):       
        cashflow_statement = self.company.cf_statements.create(
            date = csf_stt['calendarYear'],
            year = csf_stt['date'],
            reported_currency = Currency.objects.get_or_create(currency=csf_stt['reportedCurrency'])[0],
            net_income = csf_stt['netIncome'],
            depreciation_amortization = csf_stt['depreciationAndAmortization'],
            deferred_income_tax = csf_stt['deferredIncomeTax'],
            stock_based_compesation = csf_stt['stockBasedCompensation'],
            change_in_working_capital = csf_stt['changeInWorkingCapital'],
            accounts_receivables = csf_stt['accountsReceivables'],
            inventory = csf_stt['inventory'],
            accounts_payable = csf_stt['accountsPayables'],
            other_working_capital = csf_stt['otherWorkingCapital'],
            other_non_cash_items = csf_stt['otherNonCashItems'],
            operating_activities_cf = csf_stt['netCashProvidedByOperatingActivities'],
            investments_property_plant_equipment = csf_stt['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net = csf_stt['acquisitionsNet'],
            purchases_investments = csf_stt['purchasesOfInvestments'],
            sales_maturities_investments = csf_stt['salesMaturitiesOfInvestments'],
            other_investing_activites = csf_stt['otherInvestingActivites'],
            investing_activities_cf = csf_stt['netCashUsedForInvestingActivites'],
            debt_repayment = csf_stt['debtRepayment'],
            common_stock_issued = csf_stt['commonStockIssued'],
            common_stock_repurchased = csf_stt['commonStockRepurchased'],
            dividends_paid = csf_stt['dividendsPaid'],
            other_financing_activities = csf_stt['otherFinancingActivites'],
            financing_activities_cf = csf_stt['netCashUsedProvidedByFinancingActivities'],
            effect_forex_exchange = csf_stt['effectOfForexChangesOnCash'],
            net_change_cash = csf_stt['netChangeInCash'],
            cash_end_period = csf_stt['cashAtEndOfPeriod'],
            cash_beginning_period = csf_stt['cashAtBeginningOfPeriod'],
            operating_cf = csf_stt['operatingCashFlow'],
            capex = csf_stt['capitalExpenditure'],
            fcf = csf_stt['freeCashFlow'],)
        
        return cashflow_statement
    
    def create_current_stock_price(self, data:dict):
        stock_prices = self.company.stock_prices.create(**data)
        return stock_prices

    def create_rentability_ratios(self, data:dict):
        rentability_ratios = self.company.rentability_ratios.create(**data)
        return rentability_ratios

    def create_liquidity_ratio(self, data:dict):
        liquidity_ratios = self.company.liquidity_ratios.create(**data)
        return liquidity_ratios

    def create_margin_ratio(self, data:dict):
        margins = self.company.margins.create(**data)
        return margins

    def create_fcf_ratio(self, data:dict):
        fcf_ratios = self.company.fcf_ratios.create(**data)
        return fcf_ratios

    def create_ps_value(self, data:dict):
        per_share_values = self.company.per_share_values.create(**data)
        return per_share_values

    def create_non_gaap(self, data:dict):
        non_gaap_figures = self.company.non_gaap_figures.create(**data)
        return non_gaap_figures

    def create_operation_risk_ratio(self, data:dict):
        operation_risks_ratios = self.company.operation_risks_ratios.create(**data)
        return operation_risks_ratios

    def create_enterprise_value_ratio(self, data:dict):
        ev_ratios = self.company.ev_ratios.create(**data)
        return ev_ratios

    def create_company_growth(self, data:dict):
        growth_rates = self.company.growth_rates.create(**data)
        return growth_rates

    def create_eficiency_ratio(self, data:dict):
        efficiency_ratios = self.company.efficiency_ratios.create(**data)
        return efficiency_ratios

    def create_price_to_ratio(self, data:dict):
        price_to_ratios = self.company.price_to_ratios.create(**data)
        return price_to_ratios