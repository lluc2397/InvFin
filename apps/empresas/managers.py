from apps.general.managers import BaseSharedManager


class CompanyManager(BaseSharedManager):

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
            description_translated = False,
            exchange__main_org__name = name
            )        
    
    def random_clean_company(self):
        companies = self.clean_companies()
        return self.get_random(companies)
    
    def random_clean_company_by_main_exchange(self, name=None):
        companies = self.clean_companies_by_main_exchange(name)
        return self.get_random(companies)
    
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