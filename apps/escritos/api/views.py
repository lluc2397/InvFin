from rest_framework.response import Response
from rest_framework import status

from apps.api.views import BaseAPIView

from .serializers import TermSerializer, TermContent


class TermAPIView(BaseAPIView):
    serializer_class = TermSerializer
    query_name = 'slug'


class TermContentAPIView(BaseAPIView):
    serializer_class = TermContent
    queryset = TermContent