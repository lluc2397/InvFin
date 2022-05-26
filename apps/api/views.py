from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS
from rest_framework import status

from .models import Token

class CheckKey(BasePermission):
    def has_permission(self, request, view):
        key = request.GET.get('api_key')
        if key:
            return Token.objects.key_authorized(key)
        return request.method in SAFE_METHODS

class CompanyBaseAPIView(APIView):
    serializer_class = None
    permission_classes = [AllowAny|ReadOnly]

    def get(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)
        if status.is_success:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)