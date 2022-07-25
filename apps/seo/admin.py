from django.contrib import admin
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportActionModelAdmin
from import_export.resources import ModelResource

from apps.general.utils import ExportCsv

from .models import (
    MetaParameters,
    MetaParametersHistorial,
    UserCompanyVisited,
    UserJourney,
    UserPublicBlogVisited,
    UserQuestionVisited,
    UserTermVisited,
    Visiteur,
    VisiteurCompanyVisited,
    VisiteurJourney,
    VisiteurPublicBlogVisited,
    VisiteurQuestionVisited,
    VisiteurTermVisited,
    VisiteurUserRelation,
)


class BaseModelVisitedAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'model_visited',
        'visit',
        'date',
    ]


@admin.register(VisiteurCompanyVisited)
class VisiteurCompanyVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(UserCompanyVisited)
class UserCompanyVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(VisiteurPublicBlogVisited)
class VisiteurPublicBlogVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(UserPublicBlogVisited)
class UserPublicBlogVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(VisiteurQuestionVisited)
class VisiteurQuestionVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(UserQuestionVisited)
class UserQuestionVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(VisiteurTermVisited)
class VisiteurTermVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(UserTermVisited)
class UserTermVisitedAdmin(BaseModelVisitedAdmin):
    pass


@admin.register(VisiteurUserRelation)
class VisiteurUserRelationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'visiteur',
        'date',
        ]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class VisiteurJourneyResource(ModelResource):
    chunk_size = 10000
    class Meta:
        model = VisiteurJourney



@admin.register(VisiteurJourney)
class VisiteurJourneyAdmin(ImportExportActionModelAdmin):
    actions = ["export_as_csv"]
    resource_class = VisiteurJourneyResource
    list_display = [
        'id',
        'user_link',
        'date',
        'current_path',
        'comes_from'
        ]

    def user_link(self, obj):
        field = getattr(obj, 'user')
        object_name = field.object_name.lower()
        app_name = field.app_label
        args = field.id
        link = reverse(f'admin:{app_name}_{object_name}_change', args=(args,))
        return format_html(f'<a target="_blank" href="{link}">{field}</a>')
    user_link.short_description = 'user'


@admin.register(UserJourney)
class UserJourneyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_link',
        'date',
        'current_path',
        'comes_from'
        ]
    
    def user_link(self, obj):
        field = getattr(obj, 'user')
        object_name = field.object_name.lower()
        app_name = field.app_label
        args = field.id
        link = reverse(f'admin:{app_name}_{object_name}_change', args=(args,))
        return format_html(f'<a target="_blank" href="{link}">{field}</a>')
    user_link.short_description = 'user'


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

