from django.urls import path

from .views import (
    RoboAdvisorQuestionCompanyAnalysisAPIView,
    RoboAdvisorQuestionFinancialSituationAPIView,
    RoboAdvisorQuestionInvestorExperienceAPIView,
    RoboAdvisorQuestionPortfolioAssetsWeightAPIView,
    RoboAdvisorQuestionPortfolioCompositionAPIView,
    RoboAdvisorQuestionRiskAversionAPIView,
    RoboAdvisorQuestionStocksPortfolioAPIView,
)

urlpatterns =[
    path('robo-step-analysis', RoboAdvisorQuestionCompanyAnalysisAPIView.as_view(), name='analysis'),
    
    path('robo-step-financial', RoboAdvisorQuestionFinancialSituationAPIView.as_view(), name='financial'),
    path('robo-step-experience', RoboAdvisorQuestionInvestorExperienceAPIView.as_view(), name='experience'),
    path('robo-step-weights', RoboAdvisorQuestionPortfolioAssetsWeightAPIView.as_view(), name='weights'),
    
    path('robo-step-risk-aversion', RoboAdvisorQuestionRiskAversionAPIView.as_view(), name='risk-aversion'),

    path('robo-step-composition', RoboAdvisorQuestionPortfolioCompositionAPIView.as_view(), name='composition'),
    path('robo-step-stocks-portfolio', RoboAdvisorQuestionStocksPortfolioAPIView.as_view(), name='stocks-portfolio'),
    
]