from django.urls import path

from .views import (
    ExplorationView
)

app_name = "recsys"
urlpatterns = [
    path('explorador-general/', ExplorationView.as_view(), name="explorador_general"),
]