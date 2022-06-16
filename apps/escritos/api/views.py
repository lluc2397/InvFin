from apps.api.views import BaseAPIView
from apps.api.pagination import StandardResultPagination 
from apps.escritos.models import Term, TermContent

from .serializers import (
    TermSerializer, 
    TermContentSerializer,
    AllTermsSerializer
)


class AllTermsAPIView(BaseAPIView):
    serializer_class = AllTermsSerializer
    custom_queryset = Term.objects.clean_terms()
    pagination_class = StandardResultPagination
    pagination_class.default_limit=50


class TermAPIView(BaseAPIView):
    serializer_class = TermSerializer
    query_name = ['slug', 'id']


class TermContentAPIView(BaseAPIView):
    serializer_class = TermContentSerializer
    queryset = TermContent