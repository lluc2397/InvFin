from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework import status


class RetreiveUserCarteraAPIView(GenericAPIView):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'suer': request.user.username
        }
        if status.is_success:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)