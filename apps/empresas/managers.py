from django.db.models import Manager

from apps.general.managers import BaseSharedManager


class CompanyManager(BaseSharedManager):

    def clean_companies(self):
        return self.filter(
            no_incs = False,
            no_bs = False,
            no_cfs = False
        )
    
    def companies_by_main_exchange(self, name=None):
        return self.clean_companies().filter(exchange__main_org__name = name)
    
    def random_company(self, name):
        companies = self.companies_by_main_exchange(name)
        return self.get_random(companies)