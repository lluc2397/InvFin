from django.urls import path

from apps.roboadvisor.api.urls import urlpatterns

from .views import (
    RoboAdvisorResultView,
    RoboAdvisorServiceOptionView,
    RoboAdvisorServicesListView,
    RoboAdvisorUserResultsListView,
)

app_name = "roboadvisor"

urlpatterns = [
    path('roboadvisor/', RoboAdvisorServicesListView.as_view(), name="roboadvisor"),
    path('robo-options/<slug>/', RoboAdvisorServiceOptionView.as_view(), name="robo-option"),

    path('robo-result/<slug>/', RoboAdvisorResultView.as_view(), name="result"),

    path('tus-roboadvisor-resultados', RoboAdvisorUserResultsListView.as_view(), name="user-robo-results"),
] + urlpatterns
