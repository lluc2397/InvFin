from django.contrib import admin

from .models import (
    NewsletterDefaultDespedida,
    NewsletterDefaultIntroduction,
    NewsletterDefaultTitle,
    WritterNewsletterDefaultOptions,
    EmailNotification,
)

@admin.register(NewsletterDefaultDespedida)
class NewsletterDefaultDespedidaAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content',
        'times_used',
    ]


@admin.register(NewsletterDefaultIntroduction)    
class NewsletterDefaultIntroductionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content',
        'times_used',
    ]


@admin.register(NewsletterDefaultTitle)    
class NewsletterDefaultTitleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'content',
        'times_used',
    ]


@admin.register(WritterNewsletterDefaultOptions)    
class WritterNewsletterDefaultOptionsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'writter'
    ]


@admin.register(EmailNotification)    
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email_related'
    ]
