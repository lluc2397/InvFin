from rest_framework.response import Response
from rest_framework import status

from apps.api.views import BaseAPIView

from .serializers import TermSerializer, TermContent


class TermAPIView(BaseAPIView):
    serializer_class = TermSerializer
    query_name = 'slug'

    def get(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)


class TermContentAPIView(BaseAPIView):
    serializer_class = TermContent
    queryset = TermContent