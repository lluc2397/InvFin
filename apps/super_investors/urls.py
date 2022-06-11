from django.urls import path

from .views import (
    AllSuperinvestorsView,
    SuperinvestorView
)

app_name = "super_investors"
urlpatterns = [
    path('las-mejores-carteras-del-mundo/', AllSuperinvestorsView.as_view(), name="all_superinvestors"),
    path('cartera-de/<slug>/', SuperinvestorView.as_view(), name="superinvestor"),
]