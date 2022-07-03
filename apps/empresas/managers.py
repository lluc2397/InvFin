import random

from django.db.models import Manager

class CompanyManager(Manager):

    def only_essential(self):
        return self.only(
            'ticker',
            'name',
            'sector',
            'website',
            'state',
            'country',
            'ceo',
            'image',
            'city',
            'employees',
            'address',
            'zip_code',
            'cik',
            'cusip',
            'isin',
            'description',
            'ipoDate',
        )

    def prefetch_historical_data(self):
        return self.prefetch_related(
            'inc_statements',
            'balance_sheets',
            'cf_statements',
            'rentability_ratios',
            'liquidity_ratios',
            'margins',
            'fcf_ratios',
            'per_share_values',
            'non_gaap_figures',
            'operation_risks_ratios',
            'ev_ratios',
            'growth_rates',
            'efficiency_ratios',
            'price_to_ratios'
        )
    
    def fast_full(self):
        return self.prefetch_historical_data().only(
            'ticker',
            'name',
            'sector',
            'website',
            'state',
            'country',
            'ceo',
            'image',
            'city',
            'employees',
            'address',
            'zip_code',
            'cik',
            'cusip',
            'isin',
            'description',
            'ipoDate',
        )

    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)

    def companies_by_main_exchange(self, name=None):
        return self.filter(exchange__main_org__name = name)

    def clean_companies(self):
        return self.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False
        )
    
    def clean_companies_by_main_exchange(self, name=None):
        return self.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False,
            exchange__main_org__name = name
            )
        
    def complete_companies_by_main_exchange(self, name=None):
        return self.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False,
            description_translated = True,
            exchange__main_org__name = name
            )        
    
    def random_clean_company(self):
        companies = self.clean_companies()
        return self.get_random(companies)
    
    def random_clean_company_by_main_exchange(self, name=None):
        companies = self.clean_companies_by_main_exchange(name)
        company = self.get_random(companies)
        return company
    
    def random_complete_companies_by_main_exchange(self, name=None):
        companies = self.complete_companies_by_main_exchange(name)
        return self.get_random(companies)
    
    def clean_companies_to_update(self, name=None):
        return self.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False,
            exchange__main_org__name = name,
            updated=False, 
            has_error=False
            )
    
    def famous_companies(self):
        big_names = [
            'INTC',
            'AAPL',
            'GOOGL',
            'META',
            ''
        ]
    
    def get_companies_user_likes(self, user):
        pass


class CompanyUpdateLogManager(Manager):
    
    def create_log(self, company, where: str, error_message: str = None):
        had_error = False
        if error_message:
            had_error = True
        self.create(
            company=company,
            where=where,
            had_error=had_error,
            error_message=error_message,
        )