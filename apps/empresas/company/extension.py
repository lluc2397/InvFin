from django.db.models import Model

import math
from statistics import mean

from apps.general.utils import ChartSerializer
from apps.empresas.valuations import discounted_cashflow

from .retreive_data import RetreiveCompanyData


class CompanyExtended(Model, ChartSerializer):
    class Meta:
        abstract = True
    
    @property
    def show_news(self):
        return RetreiveCompanyData(self.ticker).get_news()

    def all_income_statements(self, limit) ->list:
        inc = self.inc_statements.all()
        if limit != 0:
            inc = inc[:limit]
        return inc

    def income_json(self, limit):
        inc = self.all_income_statements(limit)
        if not self.currency:
            self.currency = inc[0].reported_currency
        inc_json = {
            'currency': self.currency.currency,
            'labels': [data.date for data in inc],
            'fields': [
                {'title':'Ingresos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.revenue for data in inc]},
                {'title':'Costos de venta',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.cost_of_revenue for data in inc]},
                {'title':'Utilidad bruta',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.gross_profit for data in inc]},
                {'title':'I&D',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.rd_expenses for data in inc]},
                {'title':'Gastos administrativos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.general_administrative_expenses for data in inc]},
                {'title':'Gastos marketing',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.selling_marketing_expenses for data in inc]},
                {'title':'Gastos marketing, generales y administrativos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.sga_expenses for data in inc]},
                {'title':'Gastos otros',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.other_expenses for data in inc]},
                {'title':'Gastos operativos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.operating_expenses for data in inc]},
                {'title':'Gastos y costos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.cost_and_expenses for data in inc]},
                {'title':'Intereses',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.interest_expense for data in inc]},
                {'title':'Depreciación & Amortización',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.depreciation_amortization for data in inc]},
                {'title':'EBITDA',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.ebitda for data in inc]},
                {'title':'Ingresos de explotación',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.operating_income for data in inc]},
                {'title':'Otros Gastos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.net_total_other_income_expenses for data in inc]},
                {'title':'EBT',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.income_before_tax for data in inc]},
                {'title':'Impuestos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.income_tax_expenses for data in inc]},
                {'title':'Ingresos netos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.net_income for data in inc]},
                {'title':'Acciones en circulación',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.weighted_average_shares_outstanding for data in inc]},
                {'title':'Acciones diluidas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values' : [data.weighted_average_diluated_shares_outstanding for data in inc]},]    
            }
        return inc_json, inc
    

    
    def comparing_income_json(self, limit):
        comparing_json, inc = self.income_json(limit)
        chartData = self.generate_json(comparing_json)
        revenue_vs_net_income = self.generate_json(comparing_json, [0,18], 'bar')
        
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, inc

    def all_balance_sheets(self, limit) -> list:
        bls = self.balance_sheets.all()
        if limit != 0:
            bls = bls[:limit]
        return bls

    def balance_json(self, limit):
        bls = self.all_balance_sheets(limit)        
        bls_json = {
            'currency': self.currency.currency,
            'labels': [data.date for data in bls],
            'fields': [
                {'title':'Efectivo y equivalentes',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.cash_and_cash_equivalents for data in bls]},
                {'title':'Inversiones corto plazo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.short_term_investments for data in bls]},
                {'title':'Efectivo e inversiones corto plazo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.cash_and_short_term_investements for data in bls]},
                {'title':'Cuentas por cobrar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.net_receivables for data in bls]},
                {'title':'Inventario',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.inventory for data in bls]},
                {'title':'Otro activos corrientes',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_current_assets for data in bls]},
                {'title':'Activos corrientes totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_current_assets for data in bls]},
                {'title':'Propiedades y equipamiento',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.property_plant_equipement for data in bls]},
                {'title':'Goodwill',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.goodwill for data in bls]},
                {'title':'Activos intangibles',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.intangible_assets for data in bls]},
                {'title':'Goodwill y activos intangibles',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.goodwill_and_intangible_assets for data in bls]},
                {'title':'Inversiones a largo plazo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.long_term_investments for data in bls]},
                {'title':'Impuestos retenidos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.tax_assets for data in bls]},
                {'title':'Otros activos no corrientes',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_non_current_assets for data in bls]},
                {'title':'Activos no corrientes totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_non_current_assets for data in bls]},
                {'title':'Otros activos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_assets for data in bls]},
                {'title':'Activos totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_assets for data in bls]},
                {'title':'Cuentas por pagar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.account_payables for data in bls]},
                {'title':'Deuda a corto plazo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.shortTermDebt for data in bls]},
                {'title':'Impuestos por pagar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.taxPayables for data in bls]},
                {'title':'Ingreso diferido',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.deferredRevenue for data in bls]},
                {'title':'Otros pasivos corrientes',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_current_liabilities for data in bls]},
                {'title':'Pasivos corrientes totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_current_liabilities for data in bls]},
                {'title':'Deuda a largo plazo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.long_term_debt for data in bls]},
                {'title':'Otros ingresos por cobrar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.deferred_revenue_non_current for data in bls]},
                {'title':'Otros impuestos por pagar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.deferred_tax_liabilities_non_current for data in bls]},
                {'title':'Otros pasivos no corrientes',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_non_current_liabilities for data in bls]},
                {'title':'Pasivos no corrientes totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_non_current_liabilities for data in bls]},
                {'title':'Otros pasivos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_liabilities for data in bls]},
                {'title':'Pasivos totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_liabilities for data in bls]},
                {'title':'Ingresos para accionistas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.common_stocks for data in bls]},
                {'title':'Ganancias retenidas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.retained_earnings for data in bls]},
                {'title':'Otras pérdidas acumuladas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.accumulated_other_comprehensive_income_loss for data in bls]},
                {'title':'Otra equidad total',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.othertotal_stockholders_equity for data in bls]},
                {'title':'Equidad de los accionistas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_stockholders_equity for data in bls]},
                {'title':'Equidad y deuda totalas' ,
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_liabilities_and_stockholders_equity for data in bls]},
                {'title':'Inversiones totales',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_investments for data in bls]},
                {'title':'Deuda total',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.total_debt for data in bls]},
                {'title':'Deuda neta',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.net_debt for data in bls]},
            ]
        }
        return bls_json, bls
    

    
    def comparing_balance_json(self, limit):
        comparing_json, bls = self.balance_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, bls
	
    def all_cashflow_statements(self, limit) -> list:
        cf = self.cf_statements.all()
        if limit != 0:
            cf = cf[:limit]
        return cf
    
    def cashflow_json(self, limit):
        cf = self.all_cashflow_statements(limit)
        cf_json = {
            'currency': self.currency.currency,
            'labels': [data.date for data in cf],
            'fields': [
                {'title': 'Beneficio neto',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.net_income for data in cf]},
                {'title': 'Depreciación y amortización',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.depreciation_amortization for data in cf]},
                {'title': 'Impuesto sobre beneficio diferido',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.deferred_income_tax for data in cf]},
                {'title': 'Compensación en acciones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.stock_based_compesation for data in cf]},
                {'title': 'Cambios en working capital',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.change_in_working_capital for data in cf]},
                {'title': 'Cuentas por cobrar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.accounts_receivables for data in cf]},
                {'title': 'Inventario',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.inventory for data in cf]},
                {'title': 'Cuentas por pagar',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.accounts_payable for data in cf]},
                {'title': 'Otro working capital',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_working_capital for data in cf]},
                {'title': 'Otras utilidades no en efectivo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_non_cash_items for data in cf]},
                {'title': 'Flujo de caja de las operaciones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.operating_activities_cf for data in cf]},
                {'title': 'Inversiones en plantas y equipamiento',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.investments_property_plant_equipment for data in cf]},
                {'title': 'Adquisiciones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.acquisitions_net for data in cf]},
                {'title': 'Inversiones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.purchases_investments for data in cf]},
                {'title': 'Ingresos por venta de inversiones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.sales_maturities_investments for data in cf]},
                {'title': 'Otras inversiones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_investing_activites for data in cf]},
                {'title': 'Flujo de caja dedicado a inversiones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.investing_activities_cf for data in cf]},
                {'title': 'Pago de deudas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.debt_repayment for data in cf]},
                {'title': 'Acciones emitidas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.common_stock_issued for data in cf]},
                {'title': 'Recompra de acciones',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.common_stock_repurchased for data in cf]},
                {'title': 'Dividendos pagados',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.dividends_paid for data in cf]},
                {'title': 'Otras actividades financieras',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.other_financing_activities for data in cf]},
                {'title': 'Flujo de caja usado (proporcionado) por actividades financieras',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.financing_activities_cf for data in cf]},
                {'title': 'Efecto del cambio de divisas',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.effect_forex_exchange for data in cf]},
                {'title': 'Cambio en efectivo neto',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.net_change_cash for data in cf]},
                {'title': 'Efectivo al final del periodo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.cash_end_period for data in cf]},
                {'title': 'Efectivo al principio del periodo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.cash_beginning_period for data in cf]},
                {'title': 'Flujo de caja operativo',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.operating_cf for data in cf]},
                {'title': 'CAPEX',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.capex for data in cf]},
                {'title': 'Flujo de caja libre',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values':[data.fcf for data in cf]},]
                        }
        return cf_json, cf
    

    
    def comparing_cashflows(self, limit):
        comparing_json, cf = self.cashflow_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf

    def all_rentablity_ratios(self, limit) -> list:
        rr = self.rentability_ratios.all()
        if limit != 0:
            rr = rr[:limit]
        return rr

    def rentability_ratios_json(self, limit):
        rr = self.all_rentablity_ratios(limit)        
        rr_json = {
            'labels': [data.date for data in rr],
            'fields': [
                {
                'title': 'ROA',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.roa for data in rr]},
            {
                'title': 'ROE',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.roe for data in rr]},
            {
                'title': 'ROC',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.roc for data in rr]},
            {
                'title': 'ROCE',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.roce for data in rr]},
            {
                'title': 'ROTA',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.rota for data in rr]},
            {
                'title': 'ROIC',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.roic for data in rr]},
            {
                'title': 'NOPATROIC',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.nopatroic for data in rr]},
            {
                'title': 'ROGIC',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.rogic for data in rr]},
                            ]}
        return rr_json, rr


    
    def comparing_rentability_ratios_json(self, limit):
        comparing_json, rr = self.rentability_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, rr
    
    def all_liquidity_ratios(self, limit) -> list:
        lr = self.liquidity_ratios.all()
        if limit != 0:
            lr = lr[:limit]
        return lr

    def liquidity_ratios_json(self, limit):
        lr = self.all_liquidity_ratios(limit)        
        lr_json = {
            'labels': [data.date for data in lr],
            'fields': [
                {
                'title': 'Cash Ratio',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.cash_ratio for data in lr]},
                {
                'title': 'Current Ratio',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.current_ratio for data in lr]},
                {
                'title': 'Quick Ratio',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.quick_ratio for data in lr]},
                {
                'title': 'Operating cashflow Ratio',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.operating_cashflow_ratio for data in lr]},
                {
                'title': 'Deuda frente equidad',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.debt_to_equity for data in lr]},
            ]}
        return lr_json, lr
    

    
    def comparing_liquidity_ratios_json(self, limit):
        comparing_json, lr = self.liquidity_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, lr
    
    def all_margins(self, limit) -> list:
        margins = self.margins.all()
        if limit != 0:
            margins = margins[:limit]
        return margins

    def margins_json(self, limit):
        cf = self.all_margins(limit)
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Margen bruto',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.gross_margin for data in cf]},
                {
                'title': 'Margen EBITDA',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.ebitda_margin for data in cf]},
                {
                'title': 'Margen Beneficio neto',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.net_income_margin for data in cf]},
                {
                'title': 'FCF equidad',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.fcf_equity_to_net_income for data in cf]},
                {
                'title': 'Unlevered FCF',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.unlevered_fcf_to_net_income for data in cf]},
                {
                'title': 'Unlevered FCF EBIT to Net Income',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.unlevered_fcf_ebit_to_net_income for data in cf]},
                {
                'title': 'Owners Earnings to Net Income',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.owners_earnings_to_net_income for data in cf]},                
                {
                'title': 'Margen flujo de efectivo',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.fcf_margin for data in cf]},
            ]}
        return cf_json, cf
    
    
    def comparing_margins_json(self, limit):
        comparing_json, cf = self.margins_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf

    def all_fcf_ratios(self, limit) -> list:
        fcf_ratios = self.fcf_ratios.all()
        if limit != 0:
            fcf_ratios = fcf_ratios[:limit]
        return fcf_ratios

    def fcf_ratios_json(self, limit):
        cf = self.all_fcf_ratios(limit)        
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [{
                'title': 'FCF to equity',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.fcf_equity for data in cf]},
                {
                'title': 'Unlevered FCF',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.unlevered_fcf for data in cf]},
                {
                'title': 'Unlevered FCF EBIT',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.unlevered_fcf_ebit for data in cf]},
                {
                'title': 'Owners Earnings',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.owners_earnings for data in cf]},
            ]}
        return cf_json, cf
    
    def comparing_fcf_ratios_json(self, limit):
        comparing_json, cf = self.fcf_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf
    
    def all_per_share_values(self, limit) -> list:
        per_share_values = self.per_share_values.all()
        if limit != 0:
            per_share_values = per_share_values[:limit]
        return per_share_values

    def per_share_values_json(self, limit):
        cf = self.all_per_share_values(limit)        
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Ventas por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.sales_ps for data in cf]},
                {
                'title': 'Activos totales por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.book_ps for data in cf]},
                {
                'title': 'Valor tangible por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.tangible_ps for data in cf]},
                {
                'title': 'FCF por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.fcf_ps for data in cf]},
                {
                'title': 'Beneficio por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.eps for data in cf]},
                {
                'title': 'Efectivo por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.cash_ps for data in cf]},
                {
                'title': 'Flujo efectivo operativo por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.operating_cf_ps for data in cf]},
                {
                'title': 'CAPEX por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.capex_ps for data in cf]},
                {
                'title': 'Activos totales por acción',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.total_assets_ps for data in cf]},
            ]}
        return cf_json, cf

    
    def comparing_per_share_values_json(self, limit):
        comparing_json, cf = self.per_share_values_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf

    def all_non_gaap(self, limit) -> list:
        nongaap = self.non_gaap_figures.all()
        if limit != 0:
            nongaap = nongaap[:limit]
        return nongaap
    
    def non_gaap_json(self, limit):
        nongaap = self.all_non_gaap(limit)        
        nongaap_json = {
            'labels': [data.date for data in nongaap],
            'fields': [
                {
                'title': 'Ingresos normalizados',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.normalized_income for data in nongaap]},
                {
                'title': 'Tasa de impuestos',
                'url':"#!",
                'percent': 'true',
                'short': 'false',
                'values': [data.effective_tax_rate for data in nongaap]},
                {
                'title': 'NOPAT',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.nopat for data in nongaap]},
                {
                'title': 'Net Working capital',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.net_working_cap for data in nongaap]},
                {
                'title': 'Inventario promedio',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.average_inventory for data in nongaap]},
                {
                'title': 'Promedio cuentas por pagar',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.average_payables for data in nongaap]},
                {
                'title': 'Dividend yield',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.dividend_yield for data in nongaap]},
                {
                'title': 'Earnings yield',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.earnings_yield for data in nongaap]},
                {
                'title': 'FCF yield',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.fcf_yield for data in nongaap]},
                {
                'title': 'Calidad de los ingresos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.income_quality for data in nongaap]},
                {
                'title': 'Capital invertido',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.invested_capital for data in nongaap]},
                {
                'title': 'Capitalización bursátil',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.market_cap for data in nongaap]},
                {
                'title': 'Valor de los activos corrientes netos',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.net_current_asset_value for data in nongaap]},
                {
                'title': 'Payout ratio',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.payout_ratio for data in nongaap]},
                {
                'title': 'Valor activos tangibles',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.tangible_assets for data in nongaap]},
                {
                'title': 'Retention ratio',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.retention_ratio for data in nongaap]},
            ]}
        return nongaap_json, nongaap
    

    
    def comparing_non_gaap_json(self, limit):
        comparing_json, nongaap = self.non_gaap_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, nongaap
    
    def all_operation_risks_ratios(self, limit) -> list:
        operation_risks_ratios = self.operation_risks_ratios.all()
        if limit != 0:
            operation_risks_ratios = operation_risks_ratios[:limit]
        return operation_risks_ratios

    def operation_risks_ratios_json(self, limit):
        cf = self.all_operation_risks_ratios(limit)        
        or_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Cobertura de activos',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.asset_coverage_ratio for data in cf]},
                {
                'title': 'Cobertuda de flujo de caja',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.cashFlowCoverageRatios for data in cf]},
                {
                'title': 'Cobertuda de efectivo',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.cash_coverage for data in cf]},
                {
                'title': 'Tasa de cobertura del servicio de la deuda',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.debt_service_coverage for data in cf]},
                {
                'title': 'Cobertura de intereses',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.interestCoverage for data in cf]},
                {
                'title': 'Ratio cashflow operativo',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.operating_cashflow_ratio for data in cf]},
                {
                'title': 'Ratio de deuda',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.debtRatio for data in cf]},
                {
                'title': 'Deuda largo plazo a capitalización',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.longTermDebtToCapitalization for data in cf]},
                {
                'title': 'Deuda total a capitalización',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.totalDebtToCapitalization for data in cf]},
            ]}
        return or_json, cf
    
    
    def comparing_operation_risks_ratios_json(self, limit):
        comparing_json, cf = self.operation_risks_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf
    
    def all_ev_ratios(self, limit) -> list:
        ev_ratios = self.ev_ratios.all()
        if limit != 0:
            ev_ratios = ev_ratios[:limit]
        return ev_ratios

    def ev_ratios_json(self, limit):
        cf = self.all_ev_ratios(limit)        
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Capitalización bursátil',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.market_cap for data in cf]},
                                {
                'title': 'Enterprise value',
                'url':"#!",
                'percent': 'false',
                'short': 'false',
                'values': [data.enterprise_value for data in cf]},
                {
                'title': 'EV to free cash flow',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.ev_fcf for data in cf]},
                {
                'title': 'EV to operating cashflow',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.ev_operating_cf for data in cf]},
                {
                'title': 'EV to sales',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.ev_sales for data in cf]},
                {
                'title': 'Equity multiplier',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.company_equity_multiplier for data in cf]},
                {
                'title': 'EV multiple',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.ev_multiple for data in cf]},
            ]}
        return cf_json, cf
    
    
    def comparing_ev_ratios_json(self, limit):
        comparing_json, ev_ratios = self.ev_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, ev_ratios
    
    def all_growth_rates(self, limit) -> list:
        growth_rates = self.growth_rates.all()
        if limit != 0:
            growth_rates = growth_rates[:limit]
        return growth_rates

    def growth_rates_json(self, limit):
        cf = self.all_growth_rates(limit)
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Crecimiento de los ingresos',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.revenue_growth for data in cf]},
                {
                'title': 'Crecimiento de los costos de venta',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.cost_revenue_growth for data in cf]},
                {
                'title': 'Crecimiento de los gastos operativos',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.operating_expenses_growth for data in cf]},
                {
                'title': 'Crecimiento del beneficio neto',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.net_income_growth for data in cf]},
                {
                'title': 'Recompara de acciones',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.shares_buyback for data in cf]},
                {
                'title': 'Crecimiento del BPA',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.eps_growth for data in cf]},
                {
                'title': 'Crecimiento de los ingresos',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.fcf_growth for data in cf]},
                {
                'title': 'Crecimiento de los owners earnings',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.owners_earnings_growth for data in cf]},
                {
                'title': 'Crecimiento del CAPEX',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.capex_growth for data in cf]},
                {
                'title': 'Crecimiento del I+D',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.rd_expenses_growth for data in cf]},
            ]}
        return cf_json, cf
    
    
    def comparing_growth_rates_json(self, limit):
        comparing_json, cf = self.growth_rates_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf
    
    def all_efficiency_ratios(self, limit) -> list:
        efficiency_ratios = self.efficiency_ratios.all()
        if limit != 0:
            efficiency_ratios = efficiency_ratios[:limit]
        return efficiency_ratios

    def efficiency_ratios_json(self, limit):
        cf = self.all_efficiency_ratios(limit)        
        er_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                'title': 'Rotación de activos',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.asset_turnover for data in cf]},
                {
                'title': 'Rotación del inventario',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.inventory_turnover for data in cf]},
                {
                'title': 'Rotación de activos tangibles',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.fixed_asset_turnover for data in cf]},
                {
                'title': 'Rotación de cuentas por pagar',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.payables_turnover for data in cf]},
                {
                'title': 'Ciclo conversión de efectivo',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.cash_conversion_cycle for data in cf]},
                {
                'title': 'Inventario disponible (Días)',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.days_inventory_outstanding for data in cf]},
                {
                'title': 'Cuentas por pagar en circulación (Días)',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.days_payables_outstanding for data in cf]},
                {
                'title': 'Ventas activas (Días)',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.days_sales_outstanding for data in cf]},
                {
                'title': 'Ratio FCF a flujo de efectivo operativo',
                'url':"#!",
                'percent': 'true',
                'short': 'true',
                'values': [data.fcf_to_operating_cf for data in cf]},
                {
                'title': 'Ciclo operativo',
                'url':"#!",
                'percent': 'false',
                'short': 'true',
                'values': [data.operating_cycle for data in cf]},
            ]}
        return er_json, cf
    
    def comparing_efficiency_ratios_json(self, limit):
        comparing_json, cf = self.efficiency_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf

    def all_price_to_ratios(self, limit) -> list:
        price_to_ratios = self.price_to_ratios.all()
        if limit != 0:
            price_to_ratios = price_to_ratios[:limit]
        return price_to_ratios

    def price_to_ratios_json(self, limit):
        cf = self.all_price_to_ratios(limit)        
        cf_json = {
            'labels': [data.date for data in cf],
            'fields': [
                {
                    'title': 'Precio valor en libros',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_book for data in cf]},
                    {
                    'title': 'Precio cashflow',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_cf for data in cf]},
                    {
                    'title': 'Precio beneficio',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_earnings for data in cf]},
                    {
                    'title': 'PEG',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_earnings_growth for data in cf]},
                    {
                    'title': 'Precio por ventas',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_sales for data in cf]},
                    {
                    'title': 'Precio activos totales',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_total_assets for data in cf]},
                    {
                    'title': 'Precio FCF',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_fcf for data in cf]},
                    {
                    'title': 'Precio cashflow operativo',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_operating_cf for data in cf]},
                    {
                    'title': 'Precio activos tangibles',
                    'url':"#!",
                    'percent': 'false',
                    'short': 'true',
                    'values': [data.price_tangible_assets for data in cf]},
            ]}
        return cf_json, cf
      
    def comparing_price_to_ratios_json(self, limit):
        comparing_json, cf = self.price_to_ratios_json(limit)
        chartData = self.generate_json(comparing_json)
        data = {
            'table':comparing_json,
            'chart':chartData
        }
        return data, cf

    def important_ratios(self, limit):
        comparing_rentability_ratios_json, rentability_ratios = self.comparing_rentability_ratios_json(limit)
        comparing_liquidity_ratios_json, liquidity_ratios = self.comparing_liquidity_ratios_json(limit)
        comparing_margins_json, margins = self.comparing_margins_json(limit)

        ratios = [
            {
                'kind':'rentability',
                'title': 'Ratios de rentabilidad',
                'table': comparing_rentability_ratios_json['table'],
                'chart': comparing_rentability_ratios_json['chart']
            },
            {
                'kind':'liquidity',
                'title': 'Ratios de liquidez',
                'table': comparing_liquidity_ratios_json['table'],
                'chart': comparing_liquidity_ratios_json['chart']
            },
            {
                'kind':'margins',
                'title': 'Márgenes',
                'table': comparing_margins_json['table'],
                'chart': comparing_margins_json['chart']
            }
        ]
        query_ratios = {
            'rentability_ratios': rentability_ratios,
            'liquidity_ratios': liquidity_ratios,
            'margins': margins,
        }
        return ratios, query_ratios
    
    def secondary_ratios(self, limit):
        comparing_efficiency_ratios_json, efficiency_ratios = self.comparing_efficiency_ratios_json(limit)
        comparing_operation_risks_ratios_json, op_risk_ratios = self.comparing_operation_risks_ratios_json(limit)
        comparing_non_gaap_json, non_gaap = self.comparing_non_gaap_json(limit)
        comparing_per_share_values_json, per_share = self.comparing_per_share_values_json(limit)
        comparing_fcf_ratios_json, fcf_ratios = self.comparing_fcf_ratios_json(limit)

        ratios = [
            {
                'kind':'efficiency',
                'title': 'Ratios de eficiencia',
                'table': comparing_efficiency_ratios_json['table'],
                'chart': comparing_efficiency_ratios_json['chart']
            },
            {
                'kind':'operations',
                'title': 'Ratios de riesgo de operaciones',
                'table': comparing_operation_risks_ratios_json['table'],
                'chart': comparing_operation_risks_ratios_json['chart']
            },
            {
                'kind':'nongaap',
                'title': 'Non GAAP',
                'table': comparing_non_gaap_json['table'],
                'chart': comparing_non_gaap_json['chart']
            },
            {
                'kind':'pershare',
                'title': 'Valor por acción',
                'table': comparing_per_share_values_json['table'],
                'chart': comparing_per_share_values_json['chart']
            },
            {
                'kind':'fcfratios',
                'title': 'FCF ratios',
                'table': comparing_fcf_ratios_json['table'],
                'chart': comparing_fcf_ratios_json['chart']
            }
        ]
        query_ratios = {
            'efficiency_ratios': efficiency_ratios,
            'op_risk_ratios': op_risk_ratios,
            'non_gaap': non_gaap,
            'per_share': per_share,
            'fcf_ratios': fcf_ratios,
        }
        return ratios, query_ratios
    
    def calculate_current_ratios(
            self,
            all_balance_sheets:list=None,
            all_per_share:list=None,
            all_margins:list=None,
            all_inc_statements:list=None
        ) -> dict:
        current_price = RetreiveCompanyData(self.ticker).get_current_price()['current_price']

        all_balance_sheets = all_balance_sheets if all_balance_sheets else self.all_balance_sheets(10) 
        all_per_share = all_per_share if all_per_share else self.all_per_share_values(10) 
        all_margins = all_margins if all_margins else self.all_margins(10) 
        all_inc_statements = all_inc_statements if all_inc_statements else self.all_income_statements(10) 

        last_balance_sheet = all_balance_sheets[0]
        last_per_share = all_per_share[0]
        last_margins = all_margins[0]
        last_income_statement = all_inc_statements[0]
        last_revenue = last_income_statement.revenue
        average_shares_out = last_income_statement.weighted_average_shares_outstanding

        num_ics = 10 if len(all_inc_statements) >= 10 else len(all_inc_statements)
        number = num_ics - 1

        try:
            sharesbuyback = abs((((average_shares_out/all_inc_statements[number].weighted_average_shares_outstanding)**((1/num_ics)))-1)*100)
        except ZeroDivisionError:
            sharesbuyback = 0

        try:
            cagr = (((last_revenue/all_inc_statements[number].revenue)**((1/num_ics)))-1)*100
        except ZeroDivisionError:
            cagr = 0
        current_eps = last_per_share.eps    
        marketcap = average_shares_out * current_price

        try:
            pfcf = (current_price / last_per_share.fcf_ps)
        except ZeroDivisionError:
            pfcf = 0

        try:
            pb = (current_price / last_per_share.book_ps)
        except ZeroDivisionError:
            pb = 0

        try:
            pta = (current_price / last_per_share.tangible_ps)
        except ZeroDivisionError:
            pta = 0

        try:
            pcps = (current_price / last_per_share.cash_ps)
        except ZeroDivisionError:
            pcps = 0

        try:
            pocf = (current_price / last_per_share.operating_cf_ps)
        except ZeroDivisionError:
            pocf = 0

        try:
            per = (current_price / current_eps)
        except ZeroDivisionError:
            per = 0

        try:
            pas = (current_price / last_per_share.total_assets_ps)
        except ZeroDivisionError:
            pas=0

        try:
            peg = (per / cagr).real
        except ZeroDivisionError:
            peg =0

        try:
            ps = (current_price / last_per_share.sales_ps)
        except ZeroDivisionError:
            ps = 0

        ev = marketcap + last_balance_sheet.total_debt - last_balance_sheet.cash_and_short_term_investements

        try:
            evebitda = (ev / last_income_statement.ebitda)
        except ZeroDivisionError:
            evebitda = 0

        try:
            evsales = (ev / last_revenue)
        except ZeroDivisionError:
            evsales = 0

        gramvalu = (math.sqrt(22.5*current_eps * last_per_share.book_ps)) if current_eps > 0 else 0
        safety_margin_pes = ((gramvalu / current_price)-1)*100 if current_price !=0 else 0
        
        fair_value = discounted_cashflow(
            last_revenue = last_revenue,
            revenue_growth = cagr,
            net_income_margin = last_margins.net_income_margin,
            fcf_margin = last_margins.fcf_margin,
            buyback = sharesbuyback,
            average_shares_out = average_shares_out,
        )
        safety_margin_opt = ((fair_value / current_price)-1)*100 if current_price !=0 else 0

        if per > 30 or per <= 0: 
            per_lvl = 1 
        elif per < 30 and per > 15: 
            per_lvl = 2 
        else: 
            per_lvl = 3

        if pb > 3 or pb <= 0: 
            pb_lvl = 1 
        elif pb < 3 and pb > 2: 
            pb_lvl = 2 
        else: 
            pb_lvl = 3

        if pas > 6 or pas <= 0: 
            pas_lvl = 1 
        elif pas < 3 and pas > 2: 
            pas_lvl = 2 
        else: 
            pas_lvl = 3

        if pta > 3 or pta <= 0: 
            pta_lvl = 1 
        elif pta < 3 and pta > 2: 
            pta_lvl = 2 
        else: 
            pta_lvl = 3

        if pcps > 10 or pcps <= 0: 
            pcps_lvl = 1 
        elif pcps < 5 and pcps > 2: 
            pcps_lvl = 2 
        else: 
            pcps_lvl = 3

        if pocf > 25 or pocf <= 0: 
            pocf_lvl = 1 
        elif pocf < 18 and pocf > 10: 
            pocf_lvl = 2 
        else: 
            pocf_lvl = 3

        if peg > 2 or peg <= 0: 
            peg_lvl = 1 
        elif peg < 2 and peg > 1: 
            peg_lvl = 2 
        else: 
            peg_lvl = 3

        if ps > 4 or ps <= 0: 
            ps_lvl = 1 
        elif ps < 4 and ps > 2: 
            ps_lvl = 2 
        else: 
            ps_lvl = 3


        if pfcf > 30 or pfcf < 0: 
            pfcf_lvl = 1 
        elif pfcf < 30 and pfcf > 15: 
            pfcf_lvl = 2 
        else: 
            pfcf_lvl = 3

        if evebitda > 30 or evebitda <= 0: 
            evebitd_lvl = 1 
        elif evebitda < 30 and evebitda > 15: 
            evebitd_lvl = 2 
        else: 
            evebitd_lvl = 3

        if evsales > 4 or evsales <= 0: 
            evsales_lvl = 1 
        elif evsales < 4 and evsales > 1: 
            evsales_lvl = 2 
        else: 
            evsales_lvl = 3

        return {
            'pfcf':pfcf, 'pfcf_lvl':pfcf_lvl,
            'pas':pas, 'pas_lvl':pas_lvl,
            'pta':pta, 'pta_lvl':pta_lvl,
            'pcps':pcps, 'pcps_lvl':pcps_lvl,
            'pocf':pocf, 'pocf_lvl':pocf_lvl,
            'per':per, 'per_lvl':per_lvl,
            'pb':pb,  'pb_lvl':pb_lvl,    
            'peg':peg,'peg_lvl':peg_lvl,
            'ps':ps, 'ps_lvl':ps_lvl,
            'fair_value':fair_value,
            'ev':ev,
            'marketcap':marketcap,
            'cagr':cagr,
            'evebitda':evebitda, 
            'evebitd_lvl':evebitd_lvl,
            'evsales':evsales, 
            'evsales_lvl':evsales_lvl,
            'gramvalu':gramvalu,
            'sharesbuyback':sharesbuyback,
            'safety_margin_pes':safety_margin_pes, 
            'safety_margin_opt':safety_margin_opt,
            'current_price':current_price,
            'last_revenue':last_revenue,
            'average_shares_out':average_shares_out,
            'last_balance_sheet':last_balance_sheet,
            'last_per_share':last_per_share,
            'last_margins':last_margins,
            'last_income_statement':last_income_statement,
            # 'average_per':average_per,
            # 'average_margin':average_margin,
            # 'average_fcf_margin':average_fcf_margin
        }
  
    def complete_info(self, limit=10):        
        comparing_income_json, all_inc_statements = self.comparing_income_json(limit)
        comparing_balance_json, all_balance_sheets = self.comparing_balance_json(limit)
        comparing_cashflows, all_cashflow_statements = self.comparing_cashflows(limit)
        important_ratios, all_important_ratios = self.important_ratios(limit)
        secondary_ratios, all_secondary_ratios = self.secondary_ratios(limit)
        
        all_rentability_ratios = all_important_ratios['rentability_ratios']
        all_liquidity_ratios = all_important_ratios['liquidity_ratios']
        all_margins = all_important_ratios['margins']

        all_efficiency_ratios = all_secondary_ratios['efficiency_ratios']
        all_op_risk_ratios = all_secondary_ratios['op_risk_ratios']
        all_non_gaap = all_secondary_ratios['non_gaap']
        all_per_share = all_secondary_ratios['per_share']
        all_fcf_ratios = all_secondary_ratios['fcf_ratios']

        comparing_ev_ratios_json, all_ev_ratios = self.comparing_ev_ratios_json(limit)
        comparing_growth_rates_json, all_growth_rates = self.comparing_growth_rates_json(limit)

        marketcap = all_ev_ratios[0].market_cap
        return {
            'comparing_income_json': comparing_income_json,
            'comparing_balance_json': comparing_balance_json,
            'comparing_cashflows': comparing_cashflows,
            'important_ratios': important_ratios,
            'secondary_ratios': secondary_ratios,
            'marketcap': marketcap
        }
