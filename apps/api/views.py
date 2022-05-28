from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, status
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.seo.utils import SeoInformation

from .models import Key, ReasonKeyRequested
from .serializers import AuthKeySerializer


class ObtainAuthKey(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = AuthKeySerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        key, created = Key.objects.get_or_create(user=user)
        return Response({'token': key.key})

obtain_auth_key = ObtainAuthKey.as_view()


class BaseAPIView(APIView):
    model = None
    queryset = None
    serializer_class = None
    query_name = []
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
        if len(self.query_name) > 1:
            for q in self.query_name:
                query_value = request.GET.get(q)
                if not query_value:
                    continue
        else:
            query_value = request.GET.get(self.query_name[0])
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


@login_required
def request_API_key(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            ReasonKeyRequested.objects.create(
            user=request.user,
            description=description
            )
            key = Key.objects.create(
            user=request.user,
            ip=SeoInformation.get_client_ip(request),
            limit=250
            )
            messages.success(request, f'Gracias, tu clave ya está disponible {key.key}')
        else:
            messages.error(request, f'Oups, parece que hay un error con tu motivo')
        return redirect(reverse('users:user_inicio'))
