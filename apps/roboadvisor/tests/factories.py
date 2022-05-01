from factory import SubFactory
from factory.django import DjangoModelFactory

from django.contrib.auth import get_user_model

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

User = get_user_model()