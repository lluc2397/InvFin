from factory import SubFactory
from factory.django import DjangoModelFactory

from ..models import (
    RoboAdvisorServiceStep,
    RoboAdvisorService,
    TemporaryInvestorProfile,
    InvestorProfile,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorUserServiceActivity,
    RoboAdvisorUserServiceStepActivity
)


class RoboAdvisorServiceFactory(DjangoModelFactory):

    class Meta:
        model = RoboAdvisorService
        django_get_or_create = ["id"]


class RoboAdvisorServiceStepFactory(DjangoModelFactory):

    class Meta:
        model = RoboAdvisorServiceStep
        django_get_or_create = ["id"]