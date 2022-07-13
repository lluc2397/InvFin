from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (
    CompanyRequestAPI,
    Endpoint,
    EndpointsCategory,
    Key,
    ReasonKeyRequested,
    SuperinvestorRequestAPI,
    TermRequestAPI,
)


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'user_link', 'created']
    ordering = ['-created']
    search_fields = ['user_username']

    def user_link(self, obj):
        field = getattr(obj, 'user')
        object_name = field.object_name.lower()
        app_name = field.app_label
        args = field.id
        link = reverse(f'admin:{app_name}_{object_name}_change', args=(args,))
        return format_html(f'<a target="_blank" href="{link}">{field}</a>')
    user_link.short_description = 'user'


@admin.register(ReasonKeyRequested)
class ReasonKeyRequestedAdmin(admin.ModelAdmin):
    list_display = ['user', 'created']
    ordering = ['-created']
    search_fields = ['user_username']


class BaseRequestAPIAdmin(admin.ModelAdmin):
    list_display = ['user', 'search', 'path', 'date']
    ordering = ['-date']
    search_fields = ['user_username']


@admin.register(CompanyRequestAPI)
class CompanyRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


@admin.register(TermRequestAPI)
class TermRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


@admin.register(SuperinvestorRequestAPI)
class SuperinvestorRequestAPIAdmin(BaseRequestAPIAdmin):
    pass


@admin.register(EndpointsCategory)
class EndpointsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order', 'icon']
    list_editable = list_display[1:]


@admin.register(Endpoint)
class EndpointAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        'title',
        'title_related',
        'order',
        'url_example',
        'is_premium',
        'is_available',
        'is_deprecated',
        'version',
        'price',
    ]
    list_editable = list_display[1:]
