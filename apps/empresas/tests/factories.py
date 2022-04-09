from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.empresas.models import Company, IncomeStatement


class CompanyFactory(DjangoModelFactory):
    ticker = 'AAPL'

    class Meta:
        model = Company 

class IncomeStatementFactory(DjangoModelFactory):
    company = SubFactory(CompanyFactory)
    date = 2017

    class Meta:
        model = IncomeStatement 