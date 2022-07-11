from django.urls import path

from .views import (
    ExplorationView,
    CompaniesRecommendedSide
)

app_name = "recsys"
urlpatterns = [
    path('explorador-general/', ExplorationView.as_view(), name="explorador_general"),

    path('companies-side-user-might-like/', CompaniesRecommendedSide.as_view(), name="recommend_side_companies"),
]