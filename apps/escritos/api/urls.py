from django.urls import path

from .views import (
    TermAPIView,
    TermContentAPIView,
    AllTermsAPIView
)

urlpatterns = [
    path('lista-terminos/', AllTermsAPIView.as_view(), name='all_terms_api'),
    path('termino/', TermAPIView.as_view(), name='term_api'),
]