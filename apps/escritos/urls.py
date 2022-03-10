from django.urls import path

from .views import (
    TermDetailsView,
    GlosarioView,
    TermCorrectionView
)

app_name = "escritos"
urlpatterns = [
    
    path('diccionario-financiero/', GlosarioView.as_view(), name='glosario'),

    path('definicion/<slug>/', TermDetailsView.as_view(), name='single_term'),

    path('correction/<pk>', TermCorrectionView.as_view(), name='correction_term'),
]