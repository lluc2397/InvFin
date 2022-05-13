from django.urls import path

from .views import (
    ScreenerInicioView,
    CompanyScreenerInicioView,
    EtfScreenerInicioView,
    CompanyDetailsView,
    EtfDetailsView
)

from .api.urls import urlpatterns

# from apps.screener.api.views import CompanyBaseAPIView

# import sys, inspect

# list_of_serializers = inspect.getmembers(sys.modules['apps.empresas.api.serializers'], lambda member: inspect.isclass(member) and member.__module__ == 'apps.empresas.api.serializers')



app_name = "screener"

urlpatterns = [
    path('', ScreenerInicioView.as_view(), name="screener_inicio"),
    path('empresas-de/<name>/', CompanyScreenerInicioView.as_view(), name="companies_by"),
    path('etfs/', EtfScreenerInicioView.as_view(), name="etfs_inicio"),

    path('analisis-de/<ticker>/', CompanyDetailsView.as_view(), name="company"),
    path('analisis-etf/<ticker>/', EtfDetailsView.as_view(), name="etf"),
] + urlpatterns

# for serializer in list_of_serializers:
#     serial_name = serializer[0][:-10]
#     route = path(   
#         f'{serial_name}',
#         CompanyBaseAPIView.as_view(serializer_class = serializer[1]),
#         name=f'{serial_name}'
#     )
#     urlpatterns.append(route)
