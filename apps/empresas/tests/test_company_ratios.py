from django.test import TestCase

from .factories import CompanyFactory
from .constants import *

from apps.empresas.utils import UpdateCompany
from apps.empresas.models import Currency

class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory()
        self.company_update = UpdateCompany(self.company)
        self.company.inc_statements.create(date = 2018)
    
    def generate_data(self):
        inc = INCOME_STATEMENT[0]

        fecha = {
            'date': inc['calendarYear'],
            'year': inc['date'],
        }
        bs = BALANCE_SHEET[0]
        cf = CASHFLOW_STATEMENT[0]
        inc.update(bs)
        inc.update(cf)
        inc.update(fecha)

        last_inc = INCOME_STATEMENT[1]
        last_fecha = {
            'date': last_inc['calendarYear'],
            'year': last_inc['date'],
        }
        last_bs = BALANCE_SHEET[1]
        last_cf = CASHFLOW_STATEMENT[1]
        last_inc.update(last_bs)
        last_inc.update(last_cf)
        last_inc.update(last_fecha)

        return {
            'current':inc,
            'last':last_inc
        }
    
    def test_need_update(self):
        need_update = self.company_update.check_last_filing()
        print(need_update)

    def test_all_data(self):
        data = self.generate_data()

        current_data = self.company_update.generate_current_data(data['current'])
        last_year_data = self.company_update.last_year_data(data['last'])

        all_data = current_data
        all_data.update(last_year_data)

        main_ratios = self.company_update.calculate_main_ratios(all_data)
        all_data.update(main_ratios)

        fcf_ratio = self.company_update.calculate_fcf_ratio(current_data)
        all_data.update(fcf_ratio)

        ps_value = self.company_update.calculate_ps_value(all_data)
        all_data.update(ps_value)

        company_growth = self.company_update.calculate_company_growth(all_data)        
        all_data.update(company_growth)

        non_gaap = self.company_update.calculate_non_gaap(all_data)
        all_data.update(non_gaap)

        

        price_to_ratio = self.company_update.calculate_price_to_ratio(all_data)

        eficiency_ratio = self.company_update.calculate_eficiency_ratio(all_data)
        enterprise_value_ratio = self.company_update.calculate_enterprise_value_ratio(all_data)
        
        liquidity_ratio = self.company_update.calculate_liquidity_ratio(all_data)
        margin_ratio = self.company_update.calculate_margin_ratio(all_data)
        
        operation_risk_ratio = self.company_update.calculate_operation_risk_ratio(all_data)
        
        rentability_ratios = self.company_update.calculate_rentability_ratios(all_data)

        # self.company_update.create_current_stock_price()
        self.company_update.create_rentability_ratios(rentability_ratios)
        self.company_update.create_liquidity_ratio(liquidity_ratio)
        self.company_update.create_margin_ratio(margin_ratio)
        self.company_update.create_fcf_ratio(fcf_ratio)
        self.company_update.create_ps_value(ps_value)
        self.company_update.create_non_gaap(non_gaap)
        self.company_update.create_operation_risk_ratio(operation_risk_ratio)
        self.company_update.create_price_to_ratio(price_to_ratio)
        self.company_update.create_enterprise_value_ratio(enterprise_value_ratio)
        self.company_update.create_eficiency_ratio(eficiency_ratio)
        self.company_update.create_company_growth(company_growth)
        
        print(rentability_ratios)
        print(liquidity_ratio)
        print(margin_ratio)
        print(fcf_ratio)
        print(ps_value)
        print(non_gaap)
        print(operation_risk_ratio)
        print(price_to_ratio)
        print(enterprise_value_ratio)
        print(eficiency_ratio)
        print(company_growth)
    
        
