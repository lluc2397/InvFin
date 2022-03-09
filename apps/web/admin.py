from django.contrib import admin
from .models import WebsiteLegalPage

@admin.register(WebsiteLegalPage)
class WebsiteLegalPageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
