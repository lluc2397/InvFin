from django.urls import path

from .views import (
    TermAPIView,
    TermContentAPIView
)

urlpatterns = [
    path('termino', TermAPIView.as_view(), name='term_api'),
    path('correction', TermContentAPIView.as_view(), name='term_content_api'),
]