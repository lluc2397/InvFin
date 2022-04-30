from django.conf import settings

import requests
import yfinance as yf
import yahooquery as yq

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}

class CalculateCompanyFinancialRatios():
    def __init__(self) -> None:
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
        
    def last_year_data(self, data:dict) -> dict:
        last_year_inventory = data['inventory']
        last_year_accounts_payable = data['accountPayables']
        last_year_revenue = data['revenue']
        last_year_net_income = data['netIncome']
        last_year_fcf = data['freeCashFlow']
        last_year_capex = data['capitalExpenditure']
        last_year_shares_outstanding = data['weightedAverageShsOut']
        last_year_cost_expense = data['costAndExpenses']
        last_year_cost_revenue = data['costOfRevenue']
        last_year_eps = data['netIncome'] / data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        last_year_research_dev = data['researchAndDevelopmentExpenses']
        last_year_fixed_assets = data['propertyPlantEquipmentNet']
        last_year_assets = data['totalAssets']
        last_year_owner_earnings = data['netIncome'] + data['depreciationAndAmortization'] + data['changeInWorkingCapital'] + data['capitalExpenditure']
        last_year_current_assets = data['totalCurrentAssets']
        last_year_current_liabilities = data['totalCurrentLiabilities']
        
        result = {
            'last_year_inventory':last_year_inventory,
            'last_year_accounts_payable':last_year_accounts_payable,
            'last_year_revenue':last_year_revenue,
            'last_year_net_income':last_year_net_income,
            'last_year_fcf':last_year_fcf,
            'last_year_capex':last_year_capex,
            'last_year_shares_outstanding':last_year_shares_outstanding,
            'last_year_cost_expense':last_year_cost_expense,
            'last_year_cost_revenue':last_year_cost_revenue,
            'last_year_eps':last_year_eps,
            'last_year_research_dev':last_year_research_dev,
            'last_year_fixed_assets':last_year_fixed_assets,
            'last_year_assets':last_year_assets,
            'last_year_owner_earnings':last_year_owner_earnings,
            'last_year_current_assets':last_year_current_assets,
            'last_year_current_liabilities':last_year_current_liabilities,
        }
        return result

    def calculate_main_ratios(self, data:dict) -> dict:
        averageFxAs = ((data['last_year_fixed_assets'] + data['propertyPlantEquipmentNet'])/2)
        averageAsssets = ((data['last_year_assets'] + data['totalAssets'])/2)
        netWorkingCapital = data['totalCurrentAssets']- data['totalCurrentLiabilities']
        changeInWorkingCap = netWorkingCapital - (data['last_year_current_assets']-data['last_year_current_liabilities'])
        grossInvestedCapital = netWorkingCapital + data['propertyPlantEquipmentNet'] + data['depreciationAndAmortization']
        effectiveTaxRate = (data['incomeTaxExpense'] /data['operatingIncome']) if data['operatingIncome'] !=0 else 0
        netTangibleEquity = (data['totalCurrentAssets'] + data['propertyPlantEquipmentNet']) - data['totalLiabilities']
        nopat = data['operatingIncome'] * (1-(data['incomeTaxExpense'] /data['operatingIncome'])) if data['operatingIncome'] !=0 else 0 
        debtAndEquity = data['totalDebt'] + data['totalStockholdersEquity']
        non_cash_workcap = netWorkingCapital - data['cashAndCashEquivalents']
        investedCapital = data['propertyPlantEquipmentNet'] + non_cash_workcap

        result = {
            'averageFxAs':averageFxAs,
            'averageAsssets':averageAsssets,
            'netWorkingCapital':netWorkingCapital,
            'changeInWorkingCap':changeInWorkingCap,
            'grossInvestedCapital':grossInvestedCapital,
            'effectiveTaxRate':effectiveTaxRate,
            'netTangibleEquity':netTangibleEquity,
            'nopat':nopat,
            'debtAndEquity':debtAndEquity,
            'non_cash_workcap':non_cash_workcap,
            'investedCapital':investedCapital,
        }
        return result    

    def calculate_rentability_ratios(self, data:dict) -> dict:
        capitalEmployed = data['totalAssets'] - data['totalCurrentLiabilities']
        roa = (data['netIncome'] /  data['totalAssets'] ) *100 if data['totalAssets']  !=0 else 0
        roe = (data['netIncome'] /  data['totalStockholdersEquity'])  *100 if data['totalStockholdersEquity']  !=0 else 0
        roc = (data['operatingIncome'] /  data['totalAssets'])  *100 if data['totalAssets']  !=0 else 0
        roce = (data['operatingIncome'] /  capitalEmployed) *100 if capitalEmployed  !=0 else 0
        rota = (data['netIncome'] /  data['tangible_assets'])  *100 if data['tangible_assets']  !=0 else 0
        roic =( (data['netIncome'] - data['dividendsPaid']) /  data['investedCapital'])  *100 if data['investedCapital']  !=0 else 0
        nopatroic = (data['nopat'] /  data['investedCapital'])  *100 if data['investedCapital']  !=0 else 0
        rogic = (data['nopat'] / data['grossInvestedCapital']) *100 if data['grossInvestedCapital']  !=0 else 0

        result = {
                'roa':roa,
                'roe':roe,
                'roc':roc,
                'roce':roce,
                'rota':rota,
                'roic':roic,
                'nopatroic':nopatroic,
                'rogic':rogic,
        }
        return result

    def calculate_liquidity_ratio(self, data:dict) -> dict:
        cash_ratio = data['cashAndCashEquivalents'] / data['totalCurrentLiabilities']  if data['totalCurrentLiabilities']  !=0 else 0
        current_ratio = data['totalCurrentAssets'] / data['totalCurrentLiabilities']  if data['totalCurrentLiabilities']  !=0 else 0
        quick_ratio = (data['netReceivables'] + data['cashAndShortTermInvestments']) / data['totalCurrentLiabilities']  if data['totalCurrentLiabilities']  !=0 else 0
        operating_cashflow_ratio = data['netCashProvidedByOperatingActivities'] / data['totalCurrentLiabilities']  if data['totalCurrentLiabilities']  !=0 else 0
        debt_to_equity = data['totalLiabilities'] / data['totalStockholdersEquity']  if data['totalStockholdersEquity']  !=0 else 0

        result = {
            'cash_ratio':cash_ratio,
            'current_ratio':current_ratio,
            'quick_ratio':quick_ratio,
            'operating_cashflow_ratio':operating_cashflow_ratio,
            'debt_to_equity':debt_to_equity,
        }
        return result

    def calculate_margin_ratio(self, data:dict) -> dict:
        gross_margin = data['grossProfit'] / data['revenue'] *100 if data['revenue']  !=0 else 0
        ebitda_margin = data['ebitda'] / data['revenue'] *100 if data['revenue']  !=0 else 0
        net_income_margin = data['netIncome'] / data['revenue'] *100 if data['revenue']  !=0 else 0
        fcf_margin = data['totalLiabilities'] / data['revenue'] *100 if data['revenue']  !=0 else 0
        fcf_equity_to_net_income = data['fcf_equity']  / data['netIncome'] *100 if data['netIncome']  !=0 else 0
        unlevered_fcf_to_net_income = data['unlevered_fcf']  / data['netIncome'] *100 if data['netIncome']  !=0 else 0
        unlevered_fcf_ebit_to_net_income = data['unlevered_fcf_ebit']  / data['netIncome'] *100 if data['netIncome']  !=0 else 0
        owners_earnings_to_net_income = data['owners_earnings']  / data['netIncome'] *100 if data['netIncome']  !=0 else 0

        result = {
            'gross_margin':gross_margin,
            'ebitda_margin':ebitda_margin,
            'net_income_margin':net_income_margin,
            'fcf_margin':fcf_margin,
            'fcf_equity_to_net_income':fcf_equity_to_net_income,
            'unlevered_fcf_to_net_income':unlevered_fcf_to_net_income,
            'unlevered_fcf_ebit_to_net_income':unlevered_fcf_ebit_to_net_income,
            'owners_earnings_to_net_income':owners_earnings_to_net_income,
        }
        return result

    def calculate_fcf_ratio(self, data:dict) -> dict:
        fcf_equity = data['netCashProvidedByOperatingActivities'] + data['capitalExpenditure'] + data['debtRepayment']
        unlevered_fcf =  data['nopat'] + data['depreciationAndAmortization'] + data['changeInWorkingCapital'] + data['capitalExpenditure']
        unlevered_fcf_ebit = data['operatingIncome'] + data['depreciationAndAmortization'] + data['deferredIncomeTax'] + data['changeInWorkingCapital'] + data['capitalExpenditure']
        owners_earnings = data['netIncome'] + data['depreciationAndAmortization'] + data['changeInWorkingCapital'] + data['capitalExpenditure']

        result = {
            'fcf_equity':fcf_equity,
            'unlevered_fcf':unlevered_fcf,
            'unlevered_fcf_ebit':unlevered_fcf_ebit,
            'owners_earnings':owners_earnings,
        }
        return result

    def calculate_ps_value(self, data:dict) -> dict:
        sales_ps = data['revenue'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        book_ps = data['totalStockholdersEquity'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        tangible_ps = data['netTangibleEquity'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        fcf_ps = data['freeCashFlow'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        eps = data['netIncome'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        cash_ps = data['cashAndShortTermInvestments'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        operating_cf_ps = data['netCashProvidedByOperatingActivities'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        capex_ps = data['capitalExpenditure'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0
        total_assets_ps = data['totalAssets'] /data['weightedAverageShsOut'] if data['weightedAverageShsOut'] != 0 else 0

        result = {
            'sales_ps':sales_ps,
            'book_ps':book_ps,
            'tangible_ps':tangible_ps,
            'fcf_ps':fcf_ps,
            'eps':eps,
            'cash_ps':cash_ps,
            'operating_cf_ps':operating_cf_ps,
            'capex_ps':capex_ps,
            'total_assets_ps':total_assets_ps,
        }
        return result

    def calculate_non_gaap(self, data:dict) -> dict:                
        normalized_income = data['netIncome'] - data['totalOtherIncomeExpensesNet']
        effective_tax_rate = (data['incomeTaxExpense'] /data['operatingIncome']) if data['operatingIncome'] !=0 else 0 
        nopat = data['nopat']
        net_working_cap = data['totalCurrentAssets'] - data['totalCurrentLiabilities']
        average_inventory = ((data['last_year_inventory'] + data['inventory'])/2)
        average_payables = ((data['last_year_accounts_payable'] + data['accountPayables'])/2)
        divs_per_share = data['dividendsPaid'] / data['commonStock'] if data['commonStock'] !=0 else 0
        dividend_yield = divs_per_share / data['currentPrice'] if data['currentPrice'] !=0 else 0
        earnings_yield = (data['eps'] / data['currentPrice']) *100 if data['currentPrice'] !=0 else 0
        fcf_yield = (data['fcf_ps'] / data['currentPrice'] ) *100 if data['currentPrice'] !=0 else 0
        income_quality = (data['netCashProvidedByOperatingActivities'] /  data['netIncome'] ) *100 if data['netIncome']  !=0 else 0
        invested_capital = data['propertyPlantEquipmentNet'] + data['netWorkingCapital'] - data['cashAndCashEquivalents']
        market_cap = data['currentPrice'] * data['weightedAverageShsOut']
        net_current_asset_value = (data['totalCurrentAssets'] - (data['totalLiabilities'])) /data['weightedAverageShsOut'] if data['weightedAverageShsOut']  !=0 else 0
        payout_ratio = abs(data['dividendsPaid'] /data['netIncome']) *100 if data['netIncome'] !=0 else 0
        tangible_assets = data['totalCurrentAssets'] + data['propertyPlantEquipmentNet']
        retention_ratio = 100 - (abs(data['dividendsPaid'] /data['netIncome']) *100 if data['netIncome'] !=0 else 0)

        result = {
            'normalized_income':normalized_income,
            'effective_tax_rate':effective_tax_rate,
            'nopat':nopat,
            'net_working_cap':net_working_cap,
            'average_inventory':average_inventory,
            'average_payables':average_payables,
            'dividend_yield':dividend_yield,
            'earnings_yield':earnings_yield,
            'fcf_yield':fcf_yield,
            'income_quality':income_quality,
            'invested_capital':invested_capital,
            'market_cap':market_cap,
            'net_current_asset_value':net_current_asset_value,
            'payout_ratio':payout_ratio,
            'tangible_assets':tangible_assets,
            'retention_ratio':retention_ratio,
        }
        return result

    def calculate_operation_risk_ratio(self, data:dict) -> dict:
        asset_coverage_ratio = (data['totalAssets'] - data['goodwillAndIntangibleAssets'] - data['totalCurrentLiabilities'] - data['shortTermDebt']) / data['interestExpense'] if data['interestExpense'] != 0 else 0
        cashFlowCoverageRatios = data['netCashProvidedByOperatingActivities'] / data['totalDebt'] if data['totalDebt'] != 0 else 0
        cash_coverage = data['cashAndShortTermInvestments'] / data['interestExpense'] if data['interestExpense'] != 0 else 0
        debt_service_coverage = data['operatingIncome'] / data['totalDebt'] if data['totalDebt'] != 0 else 0
        interestCoverage = data['operatingIncome'] / data['interestExpense'] if data['interestExpense'] != 0 else 0
        operating_cashflow_ratio = data['netCashProvidedByOperatingActivities'] / data['totalCurrentLiabilities'] if data['totalCurrentLiabilities'] != 0 else 0
        debtRatio = data['totalDebt'] / data['totalAssets'] if data['totalAssets'] != 0 else 0
        longdebtandcomstock = data['longTermDebt'] + data['commonStock']
        longTermDebtToCapitalization = data['longTermDebt'] / longdebtandcomstock if longdebtandcomstock != 0 else 0
        totalDebtToCapitalization = data['totalDebt'] / data['debtAndEquity'] if data['debtAndEquity'] != 0 else 0

        result = {
            'asset_coverage_ratio':asset_coverage_ratio,
            'cashFlowCoverageRatios':cashFlowCoverageRatios,
            'cash_coverage':cash_coverage,
            'debt_service_coverage':debt_service_coverage,
            'interestCoverage':interestCoverage,
            'operating_cashflow_ratio':operating_cashflow_ratio,
            'debtRatio':debtRatio,
            'longTermDebtToCapitalization':longTermDebtToCapitalization,
            'totalDebtToCapitalization':totalDebtToCapitalization,
        }
        return result

    def calculate_enterprise_value_ratio(self, data:dict) -> dict:
        market_cap = data['currentPrice'] * data['weightedAverageShsOut']
        enterprise_value = market_cap + data['totalDebt'] - data['cashAndShortTermInvestments']
        ev_fcf = enterprise_value / data['freeCashFlow'] if data['freeCashFlow'] != 0 else 0
        ev_operating_cf = enterprise_value / data['netCashProvidedByOperatingActivities'] if data['netCashProvidedByOperatingActivities'] != 0 else 0
        ev_sales = enterprise_value / data['revenue'] if data['revenue'] != 0 else 0
        company_equity_multiplier = data['totalAssets'] / data['totalStockholdersEquity'] if data['totalStockholdersEquity'] != 0 else 0
        ev_multiple = enterprise_value / data['ebitda'] if data['ebitda'] != 0 else 0
        
        result = {
            'market_cap':market_cap,
            'enterprise_value':enterprise_value,
            'ev_fcf':ev_fcf,
            'ev_operating_cf':ev_operating_cf,
            'ev_sales':ev_sales,
            'company_equity_multiplier':company_equity_multiplier,
            'ev_multiple':ev_multiple,
        }
        return result

    def calculate_company_growth(self, data:dict) -> dict:
        revenue_growth = (data['revenue'] - data['last_year_revenue']) / data['last_year_revenue'] if data['last_year_revenue'] !=0 else 0
        cost_revenue_growth =(data['costOfRevenue'] - data['last_year_cost_revenue']) / data['last_year_cost_revenue'] if data['last_year_cost_revenue'] !=0 else 0 
        operating_expenses_growth =(data['costAndExpenses'] - data['last_year_cost_expense']) / data['last_year_cost_expense'] if data['last_year_cost_expense'] !=0 else 0 
        net_income_growth =(data['netIncome'] - data['last_year_net_income']) / data['last_year_net_income'] if data['last_year_net_income'] !=0 else 0 
        shares_buyback =(data['weightedAverageShsOut'] - data['last_year_shares_outstanding']) / data['last_year_shares_outstanding'] if data['last_year_shares_outstanding'] !=0 else 0 
        eps_growth =(data['eps'] - data['last_year_eps']) / data['last_year_eps'] if data['last_year_eps'] !=0 else 0 
        fcf_growth =(data['freeCashFlow'] - data['last_year_fcf']) / data['last_year_fcf'] if data['last_year_fcf'] !=0 else 0 
        owners_earnings_growth =(data['owners_earnings'] - data['last_year_owner_earnings']) / data['last_year_owner_earnings'] if data['last_year_owner_earnings'] !=0 else 0 
        capex_growth =(data['capitalExpenditure'] - data['last_year_capex']) / data['last_year_capex'] if data['last_year_capex'] !=0 else 0 
        rd_expenses_growth =(data['researchAndDevelopmentExpenses'] - data['last_year_research_dev']) / data['last_year_research_dev'] if data['last_year_research_dev'] !=0 else 0 

        result = {
            'revenue_growth':revenue_growth,
            'cost_revenue_growth':cost_revenue_growth,
            'operating_expenses_growth':operating_expenses_growth,
            'net_income_growth':net_income_growth,
            'shares_buyback':shares_buyback,
            'eps_growth':eps_growth,
            'fcf_growth':fcf_growth,
            'owners_earnings_growth':owners_earnings_growth,
            'capex_growth':capex_growth,
            'rd_expenses_growth':rd_expenses_growth,
        }
        return result

    def calculate_eficiency_ratio(self, data:dict) -> dict:
        days_inventory_outstanding = data['average_inventory'] / ( data['costOfRevenue'] * 360) if data['costOfRevenue']!=0 else 0
        days_payables_outstanding = (data['accountPayables'] * 360) / data['costOfRevenue'] if data['costOfRevenue']!=0 else 0
        days_sales_outstanding = (data['accountsReceivables'] *360) / data['accountPayables'] if data['accountPayables']!=0 else 0
        operating_cycle = days_inventory_outstanding + days_sales_outstanding
        cash_conversion_cycle = days_inventory_outstanding + days_sales_outstanding - days_sales_outstanding
        asset_turnover = data['revenue'] / data['averageAsssets'] if data['averageAsssets'] !=0 else 0
        inventory_turnover = data['costOfRevenue'] / data['average_inventory'] if data['average_inventory'] !=0 else 0
        fixed_asset_turnover = data['revenue'] / data['averageFxAs'] if data['averageFxAs'] !=0 else 0
        payables_turnover = data['accountPayables'] /data['average_payables'] if data['average_payables'] !=0 else 0
        fcf_to_operating_cf = data['freeCashFlow']/data['netCashProvidedByOperatingActivities'] if data['netCashProvidedByOperatingActivities'] != 0 else 0

        result = {
            'days_inventory_outstanding':days_inventory_outstanding,
            'days_payables_outstanding':days_payables_outstanding,
            'days_sales_outstanding':days_sales_outstanding,
            'operating_cycle':operating_cycle,
            'cash_conversion_cycle':cash_conversion_cycle,
            'asset_turnover':asset_turnover,
            'inventory_turnover':inventory_turnover,
            'fixed_asset_turnover':fixed_asset_turnover,
            'payables_turnover':payables_turnover,
            'fcf_to_operating_cf':fcf_to_operating_cf,
        }
        return result

    def calculate_price_to_ratio(self, data:dict) -> dict:
        price_book = data['currentPrice'] / data['book_ps'] if data['book_ps'] !=0 else 0 
        price_cf = data['currentPrice'] / data['cash_ps'] if data['cash_ps'] !=0 else 0 
        price_earnings = data['currentPrice'] / data['eps'] if data['eps'] !=0 else 0 
        price_earnings_growth =  (price_earnings / data['net_income_growth']).real if data['net_income_growth'] !=0 else 0 
        price_sales = data['currentPrice'] / data['sales_ps'] if data['sales_ps'] !=0 else 0 
        price_total_assets = data['currentPrice'] / data['total_assets_ps'] if data['total_assets_ps'] !=0 else 0 
        price_fcf = data['currentPrice'] / data['fcf_ps'] if data['fcf_ps'] !=0 else 0 
        price_operating_cf = data['currentPrice'] / data['operating_cf_ps'] if data['operating_cf_ps'] !=0 else 0 
        price_tangible_assets = data['currentPrice'] / data['tangible_ps'] if data['tangible_ps'] !=0 else 0

        result = {
            'price_book':price_book,
            'price_cf':price_cf,
            'price_earnings':price_earnings,
            'price_earnings_growth':price_earnings_growth,
            'price_sales':price_sales,
            'price_total_assets':price_total_assets,
            'price_fcf':price_fcf,
            'price_operating_cf':price_operating_cf,
            'price_tangible_assets':price_tangible_assets,
        }
        return result