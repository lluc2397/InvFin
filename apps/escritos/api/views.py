from apps.api.views import BaseAPIView
from apps.escritos.models import Term, TermContent

from .serializers import (
    TermSerializer, 
    TermContentSerializer,
    AllTermsSerializer
)


class AllTermsAPIView(BaseAPIView):
    serializer_class = AllTermsSerializer
    custom_queryset = Term.objects.clean_terms()


class TermAPIView(BaseAPIView):
    serializer_class = TermSerializer
    query_name = ['slug', 'id']


class TermContentAPIView(BaseAPIView):
    serializer_class = TermContentSerializer
    queryset = TermContent