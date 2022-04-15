from django.urls import path
from .views import (
    RoboAdvisorServicesListView,
    RoboAdvisorServiceOptionView
)

app_name = "roboadvisor"
urlpatterns =[
    path('roboadvisor/', RoboAdvisorServicesListView.as_view(), name="roboadvisor"),
    path('robo-options/<slug>/', RoboAdvisorServiceOptionView.as_view(), name="robo-option"),

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