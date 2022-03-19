from django.conf import settings

from apps.general.models import Currency
from apps.translate.google_trans_new import google_translator

from .models import (
    CashflowStatement,
    IncomeStatement,
    BalanceSheet,
    Company,
    CompanyGrowth,
    EficiencyRatio,
    EnterpriseValueRatio,
    RentabilityRatio,
    MarginRatio,
    PriceToRatio,
    LiquidityRatio,
    OperationRiskRatio,
    FreeCashFlowRatio,
    PerShareValue,
    CompanyStockPrice,
    NonGaap
)

from datetime import datetime
import yfinance as yf
import requests
from yahooquery import Ticker

FINPREP_KEY = settings.FINPREP_KEY

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

class UpdateCompany():
    def __init__(self, company) -> None:
        self.model_company = company
        self.yho_company = yf.Ticker(company.ticker)
        self.yahooquery_company = Ticker(company.ticker)


    def add_logo(self):        
        try:
            self.model_company.image = self.yho_company.info['logo_url']
            self.model_company.has_logo = True
            self.model_company.save()
        except Exception as e:
            print(e)


    def add_description(self):
        try:
            self.model_company.description = google_translator().translate(self.model_company.description,lang_src='en', lang_tgt='es')
            self.model_company.description_translated = True
            self.model_company.save()
        except Exception as e:
            print(e)


    def general_update(self):        
        if self.model_company.has_logo is False:
            self.add_logo()
        if self.model_company.description_translated is False:
            self.add_description()
        
    
    def full_general_updates(self):
        # self.general_update()
        pass



    def check_last_filing(self):
        least_recent_date = self.yahooquery_company.balance_sheet()['asOfDate'].max().value // 10**9
        least_recent_year = datetime.fromtimestamp(least_recent_date).year

        if least_recent_year != self.model_company.most_recent_year:
            print('yes')
            # self.update_income()
            # self.update_balance()
            # self.update_cashflow()


    def update_income(self):
        url_income_st = f'https://financialmodelingprep.com/api/v3/income-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'

        inc_stt = requests.get(url_income_st,headers=headers).json()[0]

        IncomeStatement.objects.create(
            company = self.model_company,
            year = datetime.strptime(inc_stt['date'], '%Y-%m-%d').date(),
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
    

    def update_balance(self):
        url_balance_sheet = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'

        bal_sht = requests.get(url_balance_sheet,headers=headers).json()[0]

        BalanceSheet.objects.create(
            company = self.model_company,
            year = datetime.strptime(bal_sht['date'], '%Y-%m-%d').date(),
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
    

    def update_cashflow(self):
        url_cashflow_st = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'

        csf_stt = requests.get(url_cashflow_st,headers=headers).json()[0]

        CashflowStatement.objects.create(
            company = self.model_company,
            year = datetime.strptime(csf_stt['date'], '%Y-%m-%d').date(),
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
    
    # def create_rentability_ratios(self):
    #     RentabilityRatio.objects.create(
    #         year = 
    #         company =
    #         roa = ''
    #         roe = ''
    #         roc = ''
    #         roce = ''
    #         rota = ''
    #         roic = ''
    #         nopatroic = ''
    #         rogic = '')

    # def create_liquidity_ratio():
    #     LiquidityRatio.objects.create(
    #         year =  
    #         company = 
    #         cash_ratio = 
    #         current_ratio = 
    #         quick_ratio = 
    #         operating_cashflow_ratio = 
    #         debt_to_equity = )

    # def create_margin_ratio():
    #     MarginRatio.objects.create(
    #         year =  
    #         company = 
    #         gross_margin = 
    #         ebitda_margin = 
    #         net_income_margin = 
    #         fcf_margin = 
    #         fcf_equity_to_net_income = 
    #         unlevered_fcf_to_net_income = 
    #         unlevered_fcf_ebit_to_net_income = 
    #         owners_earnings_to_net_income = )

    # def create_fcf_ratio():
    #     FreeCashFlowRatio.objects.create(
    #         year =  
    #         company = 
    #         fcf_equity = 
    #         unlevered_fcf = 
    #         unlevered_fcf_ebit = 
    #         owners_earnings = )

    # def create_ps_value():
    #     PerShareValue.objects.create(
    #         year =  
    #         company = 
    #         sales_ps = 
    #         book_ps = 
    #         tangible_ps = 
    #         fcf_ps = 
    #         eps = 
    #         cash_ps = 
    #         operating_cf_ps = 
    #         capex_ps = 
    #         total_assets_ps = )

    # def create_non_gaap():
    #     NonGaap.objects.create(
    #         year =  
    #         company = 
    #         normalized_income = 
    #         effective_tax_rate =     
    #         nopat = 
    #         net_working_cap = 
    #         average_inventory = 
    #         average_payables = 
    #         dividend_yield = 
    #         earnings_yield = 
    #         fcf_yield = 
    #         income_quality = 
    #         invested_capital = 
    #         market_cap = 
    #         net_current_asset_value = 
    #         payout_ratio = 
    #         tangible_assets = 
    #         retention_ratio = )

    # def create_operation_risk_ratio():
    #     OperationRiskRatio.objects.create(
    #         year =  
    #         company = 
    #         asset_coverage_ratio = 
    #         cashFlowCoverageRatios = 
    #         cash_coverage = 
    #         debt_service_coverage = 
    #         interestCoverage = 
    #         operating_cashflow_ratio = 
    #         debtRatio = 
    #         longTermDebtToCapitalization = 
    #         totalDebtToCapitalization = )

    # def create_enterprise_value_ratio():
    #     EnterpriseValueRatio.objects.create(
    #         year =  
    #         company = 
    #         market_cap = 
    #         enterprise_value = 
    #         ev_fcf = 
    #         ev_operating_cf = 
    #         ev_sales = 
    #         company_equity_multiplier = 
    #         ev_multiple = )

    # def create_company_growth():
    #     CompanyGrowth.objects.create(
    #         year =  
    #         company = 
    #         revenue_growth = 
    #         cost_revenue_growth = 
    #         operating_expenses_growth = 
    #         net_income_growth = 
    #         shares_buyback = 
    #         eps_growth = 
    #         fcf_growth = 
    #         owners_earnings_growth = 
    #         capex_growth = 
    #         rd_expenses_growth = )

    # def create_eficiency_ratio():
    #     EficiencyRatio.objects.create(
    #         year =  
    #         company = 
    #         asset_turnover = 
    #         inventory_turnover = 
    #         fixed_asset_turnover = 
    #         payables_turnover = 
    #         cash_conversion_cycle = 
    #         days_inventory_outstanding = 
    #         days_payables_outstanding = 
    #         days_sales_outstanding = 
    #         fcf_to_operating_cf = 
    #         operating_cycle = )


    # def create_price_to_ratio():
    #     PriceToRatio.objects.create(
    #         year =  
    #         company = 
    #         price_book = 
    #         price_cf = 
    #         price_earnings = 
    #         price_earnings_growth = 
    #         price_sales = 
    #         price_total_assets = 
    #         price_fcf = 
    #         price_operating_cf = 
    #         price_tangible_assets = )