from django.urls import path

from .views import (
    CompanyFODAListView,
    create_company_observation,
    get_company_news,
    suggest_list_search_companies,
    simple_valuation_view,
    medium_valuation_view,
    get_company_price,
    get_company_valuation,
    retreive_top_lists,
)


urlpatterns = [
    path('user-search-company/', suggest_list_search_companies, name="suggest_list_search_companies"),

    path('list-foda/<id>', CompanyFODAListView.as_view(), name="list_foda"),    
    path('get-company-news/<ticker>', get_company_news, name="return_company_news"),    
    path('retreive-company-price/<ticker>', get_company_price, name="get_company_price"),
    path('retreive-company-valuation/<ticker>', get_company_valuation, name="get_company_valuation"),

    path('add-observation/', create_company_observation, name="create_company_observation"),

    path('screener-simple-valuation/', simple_valuation_view, name="simple_valuation_view"),
    path('screener-medium-valuation/', medium_valuation_view, name="medium_valuation_view"),

    path('retreive-top-lists/', retreive_top_lists, name="retreive_top_lists"),
]