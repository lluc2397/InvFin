from django.urls import path

from .views import (
    CompanyFODAListView,
    CompanyObservationFormView,
    get_company_news,
    get_company_price,
    get_company_valuation,
    medium_valuation_view,
    retreive_top_lists,
    retreive_yahoo_screener_info,
    simple_valuation_view,
    suggest_list_search_companies,
    return_similar_companies_screener,
)

urlpatterns = [
    path('user-search-company/', suggest_list_search_companies, name="suggest_list_search_companies"),

    path('list-foda/<company_id>', CompanyFODAListView.as_view(), name="list_foda"),    
    path('get-company-news/<ticker>', get_company_news, name="return_company_news"),    
    path('retreive-company-price/<ticker>', get_company_price, name="get_company_price"),
    path('retreive-company-valuation/<ticker>', get_company_valuation, name="get_company_valuation"),

    path('add-observation/', CompanyObservationFormView.as_view(), name="create_company_observation"),

    path('screener-simple-valuation/', simple_valuation_view, name="simple_valuation_view"),
    path('screener-medium-valuation/', medium_valuation_view, name="medium_valuation_view"),

    path('retreive-top-lists/', retreive_top_lists, name="retreive_top_lists"),
    path('retreive-yahoo-lists/<query>', retreive_yahoo_screener_info, name="retreive_yahoo_screener_info"),

    path('return-similar-companies-screener/<sector_id>/<industry_id>/', return_similar_companies_screener, name="return_similar_companies_screener"),
]