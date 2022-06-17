from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.apps import apps
from django.views.generic import ListView
	
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers, status
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from apps.seo.utils import SeoInformation

from .models import (
    Key, 
    ReasonKeyRequested,
    EndpointsCategory
)
from .serializers import AuthKeySerializer


class ObtainAuthKey(APIView):
    throttle_classes = []
    permission_classes = []
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser]
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
    
    def get(self, request, *args, **kwargs):
        response = {
            'Respuesta': f'Autentifícate o crea un perfil para tener tu llave'
        }
        response_status = status.HTTP_204_NO_CONTENT
        if request.user.is_authenticated:
            key = Key.objects.return_if_key(user=request.user)
            if key:
                response = {
                    'Respuesta': f'Tu llave: {key}'
                }
                response_status = status.HTTP_202_ACCEPTED
        return Response(response, status=response_status)

obtain_auth_key = ObtainAuthKey.as_view()


class BaseAPIView(APIView):
    model = None
    custom_queryset = None
    custom_query = None
    serializer_class = None
    query_name = []
    fk_lookup_model = None

    def save_request(self, api_key, queryset, path, ip):
        key = Key.objects.get(key=api_key)
        queryed_model = self.serializer_class.Meta.model.__name__
        if 'Term' not in queryed_model and queryed_model != 'PublicBlog':
            queryed_model = 'Company'
        object_name = f'{queryed_model}RequestAPI'
        request_model = apps.get_model('api', object_name, require_ready=True)
        search = queryset
        if type(queryset).__name__ == 'QuerySet':
            search = None
            if 'ticker' in self.query_name and queryset[0]._meta.app_label == 'empresas':
                search = queryset[0].company
        request_data = {
            'ip': ip,
            'key': key,
            'user': key.user,
            'path': path,
            'search': search,
        }
        if queryed_model == 'Company':
            is_excel = False
            if 'company-information/excel-api' in path:
                is_excel = True
            request_data['is_excel'] = is_excel
        obj = request_model.objects.create(**request_data)
        return obj

    def get_object(self):
        if self.custom_query:
            return self.custom_query[0], self.custom_query[1]
        if self.model:
            return self.model, False
        if self.custom_queryset:
            return self.custom_queryset, True
        if not self.model and not self.custom_queryset and not self.custom_query:
            return self.serializer_class.Meta.model, False

    def final_responses(self, serializer, api_key, queryset, path, ip):
        if status.is_success:
            self.save_request(api_key, queryset, path, ip)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'Búsqueda incorrecta': 'Lo siento ha habido un problema'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    def find_query_value(self, query_dict):
        query_value = None
        query_param = None
        for query_param, query_value in query_dict.items():
            if query_param in self.query_name and query_value:
                break
        return query_param, query_value
    
    def get(self, request):
        model, many = self.get_object()
        query_dict = request.GET.dict()
        api_key = query_dict.pop('api_key')
        query_param, query_value = self.find_query_value(query_dict)
        if query_param == 'ticker':
            query_value = query_value.upper()
        if many is False:            
            if query_value:
                if self.custom_query:
                    queryset = model
                try:
                    queryset = model.objects.get(**{query_param: query_value})
                except model.DoesNotExist:
                    return Response({
                            'Búsqueda incorrecta': 'Tu búsqueda no ha devuelto ningún resultado'
                        }, 
                        status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                            'Búsqueda incorrecta': 'No has introducido ninguna búsqueda',
                            'parametros': self.query_name}, 
                        status=status.HTTP_404_NOT_FOUND)
        else:
            if self.fk_lookup_model:
                queryset = model.objects.filter(**{f'{self.fk_lookup_model}': query_value})
            else:
                queryset = model
        serializer = self.serializer_class(queryset, many=many)
        return self.final_responses(
            serializer, 
            api_key, 
            queryset, 
            request.build_absolute_uri(), 
            SeoInformation.get_client_ip(request)
        )


class APIDocumentation(ListView):
    model = EndpointsCategory
    template_name = 'explorar/api_documentation.html'
    context_object_name = "endpoints_categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = 'La mejor y más completa API de información financiera y económica'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir, API'
        context["meta_title"] = 'API documentación'
        context["meta_url"] = '/api/api-documentacion/'
        key = '*****************'
        if self.request.user.is_authenticated:
            key = Key.objects.key_for_docs(self.request.user)
        context["show_api_key"] = True if key != '*****************' else False
        context["key"] = key
        return context


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
    return redirect(request.META.get('HTTP_REFERER'))
