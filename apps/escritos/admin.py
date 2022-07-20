from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import (
    Term,
    TermContent,
    TermCorrection,
    TermsComment,
    TermsRelatedToResume,
)


@admin.action(description='Look for images')
def find_images(modeladmin, request, queryset):
    for query in queryset:
        query.save_secondary_info('term')
        query.save()


@admin.register(TermsRelatedToResume)
class TermsRelatedToResumeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'term_to_keep',
        'term_to_delete'
    ]


class TermContentInline(admin.StackedInline):
    model = TermContent


@admin.register(TermContent)
class TermContentAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]


@admin.register(Term)
class TermAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [TermContentInline]
    
    actions = [find_images]
    

    list_display = [
        'title',
        'category',
        'status',
        'total_votes',
        'total_views',
        'times_shared',        
        'published_at',
        'created_at',
        'updated_at',
    ]

    list_editable = [
        'category',
        'status',
    ]
    search_fields = ['title']


@admin.register(TermCorrection)
class TermCorrectionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]


@admin.register(TermsComment)
class TermsCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at'
    ]
    search_fields = ['author__username']
