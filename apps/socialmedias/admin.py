from django.contrib import admin

from .models import (
    LocalContentBeingShared
    )

@admin.register(LocalContentBeingShared)    
class LocalContentBeingSharedAdmin(admin.ModelAdmin):
    list_display = [
        'id'
    ]
