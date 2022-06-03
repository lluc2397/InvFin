from django.contrib import admin
from django.contrib.sessions.models import Session

from apps.general.utils import ExportCsv

from .models import (
    Visiteur,
    MetaParameters,
    MetaParametersHistorial,
    VisiteurJourney,
    UsersJourney,
    Promotion,
    PromotionCampaign,
    VisiteurUserRelation,
    VisiteurCompanyVisited,
    UserCompanyVisited,
    VisiteurPublicBlogVisited,
    UserPublicBlogVisited,
    VisiteurQuestionVisited,
    UserQuestionVisited,
    VisiteurTermVisited,
    UserTermVisited,
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


@admin.register(PromotionCampaign)
class PromotionCampaignAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'slug',
        'start_date',
        'end_date',
    ]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'slug',
        'prize',
        'has_prize',
        'shareable_url',
        'redirect_to',
        'medium',
        'web_promotion_type',
        'web_location',
        'social_media',
        'publication_date',
        'campaign_related',
        'reuse',
        'times_to_reuse',
        'clicks_by_user',
        'clicks_by_not_user',
        ]



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

