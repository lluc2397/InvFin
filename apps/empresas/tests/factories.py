from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.empresas.models import (
    Company, 
    IncomeStatement, 
    ExchangeOrganisation, 
    Exchange
)


class ExchangeOrganisationFactory(DjangoModelFactory):
    name = 'Estados Unidos'

    class Meta:
        model = ExchangeOrganisation 


class ExchangeFactory(DjangoModelFactory):
    exchange_ticker = 'NYSE'
    exchange = 'New York'
    main_org = SubFactory(ExchangeOrganisationFactory)

    class Meta:
        model = Exchange 


class CompanyFactory(DjangoModelFactory):
    ticker = 'AAPL'
    exchange = SubFactory(ExchangeFactory)

    class Meta:
        model = Company 


class IncomeStatementFactory(DjangoModelFactory):
    company = SubFactory(CompanyFactory)
    date = 2017

    class Meta:
        model = IncomeStatement 