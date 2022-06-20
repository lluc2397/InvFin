from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from apps.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import (
    Profile,
    MetaProfile,
    MetaProfileHistorial,
    CreditUsageHistorial
)

User = get_user_model()


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, auth_admin.UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            None, {"fields": ("username", "password")}
        ),
        (
            _("Type"), {"fields": ("is_writter", "just_newsletter")}
        ),
        (
            _("Personal info"), {"fields": ("first_name", "last_name", "email")}
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "is_writter", "just_newsletter", "just_correction", "last_login", "date_joined"]
    search_fields = ["first_name", "last_name", "username", "email"]
    list_editable = ['is_writter', 'just_newsletter', "just_correction"]
    list_filter = ['is_writter', 'just_newsletter', "just_correction"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'reputation_score',
        'creditos',
        'ciudad',
        'recommended_by',
        'ref_code',
    ]

    search_fields = ['user__username']
    

@admin.register(MetaProfile)
class MetaProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ip',
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
    ]


@admin.register(MetaProfileHistorial)
class MetaProfileHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'date',
        'meta_info'
    ]


@admin.register(CreditUsageHistorial)
class CreditUsageHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'date',
        'amount',
        'initial',
        'final',
        'movement',
        'move_source',
        'has_enought_credits',
    ]
