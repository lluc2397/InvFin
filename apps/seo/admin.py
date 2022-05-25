from django.contrib import admin
from django.contrib.sessions.models import Session

from apps.general.utils import ExportCsv

from .models import (
    Visiteur,
    MetaParameters,
    MetaParametersHistorial,
    VisiteurJourney,
    UsersJourney
)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


@admin.register(VisiteurJourney)
class VisiteurJourneyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
        'current_path',
        'comes_from'
        ]


@admin.register(UsersJourney)
class UsersJourneyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'date',
        'current_path',
        'comes_from'
        ]


@admin.register(Visiteur)
class VisiteurAdmin(admin.ModelAdmin, ExportCsv):
    actions = ["export_as_csv"]
    list_display = [
        'id',
        'ip',
        'session_id',
        'HTTP_USER_AGENT',
        'country_code',
        'country_name',
        'dma_code',
        'is_in_european_union',
        'latitude',
        'longitude',
        'city',
        'region',
        'time_zone',
        'postal_code',
        'continent_code',
        'continent_name',
        'first_visit_date',
    ]
    list_filter = ['country_code', 'continent_code',]
    search_fields = ['id']


@admin.register(MetaParameters)
class MetaParametersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'meta_title',
        'meta_author'
    ]


@admin.register(MetaParametersHistorial)
class MetaParametersHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'parameter_settings',
        'in_use'
    ]
    list_editable = ['in_use']

