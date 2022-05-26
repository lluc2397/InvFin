from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class BaseAPIView(APIView):
    model = None
    queryset = None
    serializer_class = None
    query_name = None
    fk_lookup_model = None

    def get_object(self):
        if self.serializer_class:
            return self.serializer_class.Meta.model, False
        else:
            if self.model:
                return self.model, False
            return self.queryset, True

    def custom_responses(self, serializer):
        if status.is_success:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def get(self, request):
        query_value = request.GET.get(self.query_name)
        if query_value:
            model, many = self.get_object()
            if many is False:
                try:
                    queryset = model.objects.get(**{self.query_name: query_value})
                except model.DoesNotExist:
                    return Response(
                        {'Búsqueda incorrecta': 'Asegúrate de usar una búsqueda correcta'}, 
                        status=status.HTTP_204_NO_CONTENT
                    )
            else:
                queryset = model.objects.filter(**{f'{self.fk_lookup_model}': query_value})
            serializer = self.serializer_class(queryset, many=many)
            self.custom_responses(serializer)
        return Response(
                        {'Búsqueda incorrecta': 'No has introducido ninguna búsqueda'}, 
                        status=status.HTTP_204_NO_CONTENT
                    )

class CompanyBaseAPIView(BaseAPIView):
    serializer_class = None

    def get(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)
        