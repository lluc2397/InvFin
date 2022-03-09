from django.contrib import admin
from .models import (
    TermContent,
    Term,
    TermCorrection,
    TermsComment,
    TermsRelatedToResume
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
class TermContentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title'
    ]


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    inlines = [TermContentInline]
    
    actions = [find_images]

    list_display = [
        'id',
        'title',
        'slug',
        'created_at',
        'updated_at',
        'total_votes',
        'total_views',
        'times_shared',
        'category',
        'author',
        'published_at',
        'status',
        'meta_information',
    ]

    list_editable = [
        'category',
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
