from django.test import TestCase

from .factories import CompanyFactory
from .constants import *

from apps.empresas.utils import UpdateCompany

class CompanyTest(TestCase):
    def setUp(self) -> None:
        self.company = CompanyFactory()
        self.company_update = UpdateCompany(self.company)
        self.company.inc_statements.create(date = 2018)
        self.company2 = CompanyFactory()
        self.company2_update = UpdateCompany(self.company2)
        self.company2.inc_statements.create(date = 2021)
    
    def test_need_update(self):
        need_update = self.company_update.check_last_filing()
        self.assertEqual(need_update, 'need update')
        
        need_update2 = self.company2_update.check_last_filing()
        self.assertEqual(need_update2, 'updated')

    def test_all_data(self):
        income_statements, balance_sheets, cashflow_statements = INCOME_STATEMENT, BALANCE_SHEET, CASHFLOW_STATEMENT

        current_data = self.company_update.generate_current_data(income_statements, balance_sheets, cashflow_statements)
        last_year_data = self.company_update.generate_last_year_data(income_statements, balance_sheets, cashflow_statements)

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

        self.assertEqual(self.company.inc_statements.count(), 1)
        self.assertEqual(self.company.stock_prices.count(), 0)
        self.assertEqual(self.company.rentability_ratios.count(), 0)
        self.assertEqual(self.company.liquidity_ratios.count(), 0)
        self.assertEqual(self.company.margins.count(), 0)
        self.assertEqual(self.company.fcf_ratios.count(), 0)
        self.assertEqual(self.company.per_share_values.count(), 0)
        self.assertEqual(self.company.non_gaap_figures.count(), 0)
        self.assertEqual(self.company.operation_risks_ratios.count(), 0)
        self.assertEqual(self.company.price_to_ratios.count(), 0)
        self.assertEqual(self.company.ev_ratios.count(), 0)
        self.assertEqual(self.company.efficiency_ratios.count(), 0)
        self.assertEqual(self.company.growth_rates.count(), 0)

        created_current_stock_price = self.company_update.create_current_stock_price(price = current_data['currentPrice'])
        created_rentability_ratios = self.company_update.create_rentability_ratios(rentability_ratios)
        created_liquidity_ratio = self.company_update.create_liquidity_ratio(liquidity_ratio)
        created_margin_ratio = self.company_update.create_margin_ratio(margin_ratio)
        created_fcf_ratio = self.company_update.create_fcf_ratio(fcf_ratio)
        created_ps_value = self.company_update.create_ps_value(ps_value)
        created_non_gaap = self.company_update.create_non_gaap(non_gaap)
        created_operation_risk_ratio = self.company_update.create_operation_risk_ratio(operation_risk_ratio)
        created_price_to_ratio = self.company_update.create_price_to_ratio(price_to_ratio)
        created_enterprise_value_ratio = self.company_update.create_enterprise_value_ratio(enterprise_value_ratio)
        created_eficiency_ratio = self.company_update.create_eficiency_ratio(eficiency_ratio)
        created_company_growth = self.company_update.create_company_growth(company_growth)
        
        self.assertEqual(created_current_stock_price.price, current_data['currentPrice'])

        self.assertEqual(self.company.stock_prices.latest().price, current_data['currentPrice'])
        self.assertEqual(self.company.rentability_ratios.latest(), created_rentability_ratios)
        self.assertEqual(self.company.liquidity_ratios.latest(), created_liquidity_ratio)
        self.assertEqual(self.company.margins.latest(), created_margin_ratio)
        self.assertEqual(self.company.fcf_ratios.latest(), created_fcf_ratio)
        self.assertEqual(self.company.per_share_values.latest(), created_ps_value)
        self.assertEqual(self.company.non_gaap_figures.latest(), created_non_gaap)
        self.assertEqual(self.company.operation_risks_ratios.latest(), created_operation_risk_ratio)
        self.assertEqual(self.company.price_to_ratios.latest(), created_price_to_ratio)
        self.assertEqual(self.company.ev_ratios.latest(), created_enterprise_value_ratio)
        self.assertEqual(self.company.efficiency_ratios.latest(), created_eficiency_ratio)
        self.assertEqual(self.company.growth_rates.latest(), created_company_growth)

        self.assertEqual(self.company.stock_prices.count(), 1)
        self.assertEqual(self.company.rentability_ratios.count(), 1)
        self.assertEqual(self.company.liquidity_ratios.count(), 1)
        self.assertEqual(self.company.margins.count(), 1)
        self.assertEqual(self.company.fcf_ratios.count(), 1)
        self.assertEqual(self.company.per_share_values.count(), 1)
        self.assertEqual(self.company.non_gaap_figures.count(), 1)
        self.assertEqual(self.company.operation_risks_ratios.count(), 1)
        self.assertEqual(self.company.price_to_ratios.count(), 1)
        self.assertEqual(self.company.ev_ratios.count(), 1)
        self.assertEqual(self.company.efficiency_ratios.count(), 1)
        self.assertEqual(self.company.growth_rates.count(), 1)

        # print(rentability_ratios)
        # print(liquidity_ratio)
        # print(margin_ratio)
        # print(fcf_ratio)
        # print(ps_value)
        # print(non_gaap)
        # print(operation_risk_ratio)
        # print(price_to_ratio)
        # print(enterprise_value_ratio)
        # print(eficiency_ratio)
        # print(company_growth)
    
        
