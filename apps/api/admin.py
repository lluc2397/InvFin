from django.contrib import admin

from .models import(
    Key,
    ReasonKeyRequested,
    CompanyRequestAPI,
    TermRequestAPI,
    Endpoint,
    EndpointsCategory
)


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ['key', 'user', 'created']
    ordering = ['-created']
    search_fields = ['user_username']


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


@admin.register(EndpointsCategory)
class EndpointsCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'order']
    list_editable = list_display[1:]


@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
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
