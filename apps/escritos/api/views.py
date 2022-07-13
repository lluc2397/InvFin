from apps.api.pagination import StandardResultPagination
from apps.api.views import BaseAPIView
from apps.escritos.models import Term, TermContent

from .serializers import AllTermsSerializer, TermContentSerializer, TermSerializer


class AllTermsAPIView(BaseAPIView):
    serializer_class = AllTermsSerializer
    custom_queryset = Term.objects.clean_terms()
    pagination_class = StandardResultPagination


class TermAPIView(BaseAPIView):
    serializer_class = TermSerializer
    query_name = ['slug', 'id']


class TermContentAPIView(BaseAPIView):
    serializer_class = TermContentSerializer
    queryset = TermContent