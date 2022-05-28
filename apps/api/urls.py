from django.conf import settings
from django.urls import include, path

from .views import request_API_key


API_version = settings.API_VERSION['CURRENT_VERSION']

app_name = "api"
urlpatterns = [
    path(f"{API_version}/", include("apps.escritos.api.urls")),
    path(f"{API_version}/", include("apps.empresas.api.urls")),

    path('request-api-key', request_API_key, name="request_api_key"),
]
