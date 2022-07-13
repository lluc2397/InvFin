from factory import SubFactory
from factory.django import DjangoModelFactory

from ..models import (
    InvestorProfile,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorService,
    RoboAdvisorServiceStep,
    RoboAdvisorUserServiceActivity,
    RoboAdvisorUserServiceStepActivity,
    TemporaryInvestorProfile,
)


class RoboAdvisorServiceFactory(DjangoModelFactory):

    class Meta:
        model = RoboAdvisorService
        django_get_or_create = ["id"]


class RoboAdvisorServiceStepFactory(DjangoModelFactory):

    class Meta:
        model = RoboAdvisorServiceStep
        django_get_or_create = ["id"]