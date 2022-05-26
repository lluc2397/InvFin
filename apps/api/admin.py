from django.contrib import admin

from .models import(
    Key,
    ReasonKeyRequested,
    CompanyRequestAPI,
    TermRequestAPI
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


@admin.register(CompanyRequestAPI)
class CompanyRequestAPIAdmin(admin.ModelAdmin):
    list_display = ['user', 'search', 'date']
    ordering = ['-date']
    search_fields = ['user_username']


@admin.register(TermRequestAPI)
class TermRequestAPIAdmin(admin.ModelAdmin):
    list_display = ['user', 'search', 'date']
    ordering = ['-date']
    search_fields = ['user_username']