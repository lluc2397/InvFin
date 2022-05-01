from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.tests.factories import UserFactory
from apps.empresas.tests.factories import CompanyFactory

from ..api.views import (
    RoboAdvisorQuestionCompanyAnalysisAPIView,
    RoboAdvisorQuestionFinancialSituationAPIView,
    RoboAdvisorQuestionInvestorExperienceAPIView,
    RoboAdvisorQuestionPortfolioAssetsWeightAPIView,
    RoboAdvisorQuestionPortfolioCompositionAPIView,
    RoboAdvisorQuestionRiskAversionAPIView,
    RoboAdvisorQuestionStocksPortfolioAPIView
)

from ..views import RoboAdvisorResultView

from .factories import 

class InvoicesAllAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.company = CompanyFactory()
    
    def test_roboadvisor_question_company_analysis_API_view(self):
        url = f'robo-step-analysis'

    def test_roboadvisor_question_financial_situation_API_view(self):
        url = f'robo-step-financial'

    def test_roboadvisor_question_investor_experience_API_view(self):
        url = f'robo-step-experience'

    def test_roboadvisor_question_portfolio_assets_weight_API_view(self):
        url = f'robo-step-weights'

    def test_roboadvisor_question_portfolio_composition_API_view(self):
        url = f'robo-step-composition'

    def test_roboadvisor_question_risk_aversion_API_view(self):
        url = f'robo-step-risk-aversion'

    def test_roboadvisor_question_stocks_portfolio_API_view(self):
        url = f'robo-step-stocks-portfolio'
    
    def test_roboadvisor_result(self):
        slug = ''
        url = f'robo-result/{slug}/'
