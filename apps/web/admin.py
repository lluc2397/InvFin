from django.contrib import admin
from .models import WebsiteLegalPage, WebsiteEmailTrack, WebsiteEmail, WebsiteEmailsType

@admin.register(WebsiteLegalPage)
class WebsiteLegalPageAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]


@admin.register(WebsiteEmailTrack)
class WebsiteEmailTrackAdmin(admin.ModelAdmin):
    list_display = ["id", "email_related", "opened", "sent_to"]


@admin.register(WebsiteEmail)
class WebsiteEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "type_related"]


@admin.register(WebsiteEmailsType)
class WebsiteEmailsTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]