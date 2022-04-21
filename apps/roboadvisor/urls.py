from django.urls import path
from .views import (
    RoboAdvisorServicesListView,
    RoboAdvisorServiceOptionView    
)

from apps.roboadvisor.api.views import (
    RoboAdvisorQuestionCompanyAnalysisAPIView,
    RoboAdvisorQuestionStocksPortfolioAPIView,
    RoboAdvisorQuestionFinancialSituationAPIView,
    RoboAdvisorQuestionInvestorExperienceAPIView,
    RoboAdvisorQuestionPortfolioAssetsWeightAPIView,
    RoboAdvisorQuestionPortfolioCompositionAPIView,
    RoboAdvisorQuestionRiskAversionAPIView
)


app_name = "roboadvisor"

urlpatterns =[
    path('roboadvisor/', RoboAdvisorServicesListView.as_view(), name="roboadvisor"),
    path('robo-options/<slug>/', RoboAdvisorServiceOptionView.as_view(), name="robo-option"),

    path('robo-step-analysis', RoboAdvisorQuestionCompanyAnalysisAPIView.as_view(), name='analysis'),
    
    path('robo-step-financial', RoboAdvisorQuestionFinancialSituationAPIView.as_view(), name='financial'),
    path('robo-step-experience', RoboAdvisorQuestionInvestorExperienceAPIView.as_view(), name='experience'),
    path('robo-step-weights', RoboAdvisorQuestionPortfolioAssetsWeightAPIView.as_view(), name='weights'),
    
    path('robo-step-risk-aversion', RoboAdvisorQuestionRiskAversionAPIView.as_view(), name='risk-aversion'),

    path('robo-step-composition', RoboAdvisorQuestionPortfolioCompositionAPIView.as_view(), name='composition'),
    path('robo-step-stocks-portfolio', RoboAdvisorQuestionStocksPortfolioAPIView.as_view(), name='stocks-portfolio'),

    # path('robo-vote/<id>', TEST_IS_USEFUL, name="robo-vote"),
    # path('favorite-stock/', STOCK_FAVORITE, name="favorite-stock"),
    # path('favorite-etf/', ETF_FAVORITE, name="favorite-etf"),



    # path('add-stock/', ADD_STOCK_PORTFOLIO, name="add-stock"),
    # path('update-stock/<pk>', UPDATE_STOCK_PORTFOLIO, name="update-stock"),
    # path('delete-stock/<pk>', DELETE_STOCK_PORTFOLIO, name="delete-stock"),
    # path('portfolio-stock-form/', PORTFOLIO_STOCK_FORM, name='portfolio-stock-form'),
    # path('portfolio-stock-details/<pk>', PORTFOLIO_STOCK_DETAILS, name="portfolio-stock-details"),

    # path('add-etf/', ADD_ETF_PORTFOLIO, name="add-etf"),
    # path('update-etf/<pk>', UPDATE_ETF_PORTFOLIO, name="update-etf"),
    # path('delete-etf/<pk>', DELETE_ETF_PORTFOLIO, name="delete-etf"),
    # path('portfolio-etf-form/', PORTFOLIO_ETF_FORM, name='portfolio-etf-form'),
    # path('portfolio-etf-details/<pk>', PORTFOLIO_ETF_DETAILS, name="portfolio-etf-details"),
    
]
