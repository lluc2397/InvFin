from django.test import TestCase

from apps.empresas.company.update import UpdateCompany
from apps.empresas.models import Company

from .constants import *
from .factories import CompanyFactory, ExchangeFactory, ExchangeOrganisationFactory


class CompanyManagersTest(TestCase):
    def setUp(self) -> None:
        self.fr_main = ExchangeOrganisationFactory(
            name='France'
        )
        self.usa_main = ExchangeOrganisationFactory(
            name='Estados Unidos'
        )
        self.nyse = ExchangeFactory(
            exchange_ticker='NYSE',
            main_org=self.usa_main
        )
        
        self.euro = ExchangeFactory(
            exchange_ticker='EURO',
            main_org=self.fr_main
        )
        self.apple = CompanyFactory(
            no_incs=True,
            no_bs=True,
            no_cfs=True,
            exchange=self.nyse
        )
        self.zinga = CompanyFactory(
            ticker='ZNGA',
            exchange=self.nyse
        )
        self.intel = CompanyFactory(
            ticker='INTC',
            exchange=self.euro
        )
        
        
    
    def test_clean_companies(self):
        all_clean = Company.objects.clean_companies()
        all_clean_by_exchange = Company.objects.clean_companies_by_main_exchange('France')
        random_clean = Company.objects.random_clean_company()

        print(all_clean)
        print(all_clean_by_exchange)
        print(random_clean)

        self.assertEqual(all_clean.count(), 2)

        self.assertEqual(all_clean_by_exchange.count(), 1)