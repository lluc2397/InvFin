from django.urls import path

from .views import (
    CompaniesRecommendedSide, 
    ExplorationView,
    RecommendationClickedRedirectView
)

app_name = "recsys"
urlpatterns = [
    path('explorador-general/', ExplorationView.as_view(), name="explorador_general"),

    path('redirect-to-recommedation/<pk>/<object_name>/', RecommendationClickedRedirectView.as_view(), name="recommendation_clicked"),

    path(
        'companies-side-user-might-like/', 
        CompaniesRecommendedSide.as_view(), 
        name="recommend_side_companies"
    ),
]