from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin

from .models import (
    FollowingHistorial,
    NewsletterFollowers,
    PublicBlog,
    PublicBlogAsNewsletter,
    PublicBlogComment,
    WritterProfile,
)


@admin.register(NewsletterFollowers)
class NewsletterFollowersAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user'
    ]


@admin.register(WritterProfile)
class WritterProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'host_name',
        'created_at'
    ]

    search_fields = ['user_username']


@admin.register(FollowingHistorial)
class FollowingHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_following',
        'user_followed',
        'started_following',
        'stop_following',
        'date',
    ]

    search_fields = ['user_followed_username']
    list_filter = [
        'started_following',
        'stop_following',
    ]


@admin.action(description='Look for images')
def find_images(modeladmin, request, queryset):
    for query in queryset:
        query.save_secondary_info('blog')
        query.save()


class NewsletterInline(admin.StackedInline):
    model = PublicBlogAsNewsletter


@admin.register(PublicBlog)
class PublicBlogAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [NewsletterInline]

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
    search_fields = ['author_username']


@admin.register(PublicBlogAsNewsletter)    
class PublicBlogAsNewsletterAdmin(admin.ModelAdmin):
    list_display = [
        'id',
    ]


@admin.register(PublicBlogComment)
class PublicBlogCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at'
    ]
