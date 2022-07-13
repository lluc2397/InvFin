from django.urls import path

from .views import (
    AllSuperinvestorsAPIView,
    SuperinvestorActivityAPIView,
    SuperinvestorHistoryAPIView,
)

urlpatterns = [
    
    path('lista-movimientos/', SuperinvestorActivityAPIView.as_view()),
    path('lista-superinversores/', AllSuperinvestorsAPIView.as_view()),
    path('lista-historial/', SuperinvestorHistoryAPIView.as_view()),
]