import random
import time

from django.conf import settings

from apps.general.models import Currency
from apps.translate.google_trans_new import google_translator

from .ratios import CalculateCompanyFinancialRatios

from datetime import datetime
import requests
import yfinance as yf
import yahooquery as yq

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}


class UpdateCompany(CalculateCompanyFinancialRatios):
    def __init__(self, company) -> None:
        self.company = company
        self.ticker = self.company.ticker
        self.finprep_key = settings.FINPREP_KEY
        self.yf_company = yf.Ticker(self.ticker)
        self.yq_company = yq.Ticker(self.ticker)
    
    def request_income_statements_finprep(self) -> list:
        url_income_st = f'https://financialmodelingprep.com/api/v3/income-statement/{self.ticker}?limit=120&apikey={self.finprep_key}'
        inc_stt = requests.get(url_income_st,headers=HEADERS).json()
        return inc_stt

    def request_balance_sheets_finprep(self) -> list:
        url_balance_sheet = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{self.ticker}?limit=120&apikey={self.finprep_key}'
        bal_sht = requests.get(url_balance_sheet,headers=HEADERS).json()
        return bal_sht

    def request_cashflow_statements_finprep(self) -> list:
        url_cashflow_st = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{self.ticker}?limit=120&apikey={self.finprep_key}'
        csf_stt = requests.get(url_cashflow_st,headers=HEADERS).json()
        return csf_stt
    
    def get_most_recent_price(self) -> float:
        if 'currentPrice' in self.yf_company.info:
            current_price = self.yf_company.info['currentPrice']
        else:
            current_price = self.yq_company.financial_data['currentPrice']
        return {'currentPrice':current_price}

    def add_logo(self):        
        try:
            self.company.image = self.yf_company.info['logo_url']
            self.company.has_logo = True
            self.company.save()
        except Exception as e:
            print(e)

    def add_description(self):
        try:
            self.company.description = google_translator().translate(self.company.description, lang_src='en', lang_tgt='es')
            self.company.description_translated = True
            self.company.save()
        except Exception as e:
            print(e)

    def general_update(self):        
        if self.company.has_logo is False:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()
    
    def financial_update(self):
        if self.check_last_filing() == 'need update':
            try:
                random_int = random.randint(5,10)
                income_statements = self.request_income_statements_finprep()
                time.sleep(random_int)
                balance_sheets = self.request_balance_sheets_finprep()
                time.sleep(random_int)
                cashflow_statements = self.request_cashflow_statements_finprep()

                current_data = self.generate_current_data(income_statements, balance_sheets, cashflow_statements)
                ly_data = self.generate_last_year_data(income_statements, balance_sheets, cashflow_statements)

                all_data = current_data
                all_data.update(ly_data)

                main_ratios = self.calculate_main_ratios(all_data)
                all_data.update(main_ratios)

                fcf_ratio = self.calculate_fcf_ratio(current_data)
                all_data.update(fcf_ratio)

                ps_value = self.calculate_ps_value(all_data)
                all_data.update(ps_value)

                company_growth = self.calculate_company_growth(all_data)        
                all_data.update(company_growth)

                non_gaap = self.calculate_non_gaap(all_data)
                all_data.update(non_gaap)

                price_to_ratio = self.calculate_price_to_ratio(all_data)
                eficiency_ratio = self.calculate_eficiency_ratio(all_data)
                enterprise_value_ratio = self.calculate_enterprise_value_ratio(all_data)
                liquidity_ratio = self.calculate_liquidity_ratio(all_data)
                margin_ratio = self.calculate_margin_ratio(all_data)
                operation_risk_ratio = self.calculate_operation_risk_ratio(all_data)
                rentability_ratios = self.calculate_rentability_ratios(all_data)
            except Exception as e:
                self.company.has_error = True
                self.company.error_message = e
                self.company.save(update_fields=['has_error', 'error_message'])
            else:
                try:
                    self.create_current_stock_price(price = current_data['currentPrice'])
                    self.create_rentability_ratios(rentability_ratios)
                    self.create_liquidity_ratio(liquidity_ratio)
                    self.create_margin_ratio(margin_ratio)
                    self.create_fcf_ratio(fcf_ratio)
                    self.create_ps_value(ps_value)
                    self.create_non_gaap(non_gaap)
                    self.create_operation_risk_ratio(operation_risk_ratio)
                    self.create_price_to_ratio(price_to_ratio)
                    self.create_enterprise_value_ratio(enterprise_value_ratio)
                    self.create_eficiency_ratio(eficiency_ratio)
                    self.create_company_growth(company_growth)

                    self.company.updated = True
                    self.company.last_update = datetime.now()
                    self.company.save(update_fields=['updated', 'last_update'])
                except Exception as e:
                    self.company.has_error = True
                    self.company.error_message = e
                    self.company.save(update_fields=['has_error', 'error_message'])
        else:
            from apps.empresas.tasks import update_company_financials_task
            self.company.date_updated = True
            self.company.save(update_fields=['date_updated'])
            update_company_financials_task.delay()

    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()['asOfDate'].max().value // 10**9 # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            print('need update', self.company)
            return 'need update'
        print('already updated', self.company)
        return 'updated'
    
    def generate_current_data(
        self,
        income_statements: list,
        balance_sheets: list,
        cashflow_statements: list
    )-> dict:

        current_data = {}
        current_price = self.get_most_recent_price()
        current_income_statements = income_statements[0]
        current_balance_sheets = balance_sheets[0]
        current_cashflow_statements = cashflow_statements[0]
        current_fecha = {
            'date': current_income_statements['calendarYear'],
            'year': current_income_statements['date'],
        }
        current_data.update(current_price)
        current_data.update(current_income_statements)
        current_data.update(current_balance_sheets)
        current_data.update(current_cashflow_statements)
        current_data.update(current_fecha)

        return current_data
    
    def generate_last_year_data(
        self,
        income_statements: list,
        balance_sheets: list,
        cashflow_statements: list
    )-> dict:

        ly_data = {}
        ly_income_statements = income_statements[1]
        ly_balance_sheets = balance_sheets[1]
        ly_cashflow_statements = cashflow_statements[1]
        ly_fecha = {
        'date': ly_income_statements['calendarYear'],
        'year': ly_income_statements['date'],
        }
        ly_data.update(ly_income_statements)
        ly_data.update(ly_balance_sheets)
        ly_data.update(ly_cashflow_statements)
        ly_data.update(ly_fecha)

        return self.last_year_data(ly_data)

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
    
    def create_current_stock_price(self, price):
        stock_prices = self.company.stock_prices.create(price=price)
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