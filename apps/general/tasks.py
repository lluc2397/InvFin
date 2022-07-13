from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.public_blog.models import (
    NewsletterFollowers,
    PublicBlog,
    PublicBlogAsNewsletter,
)
from config import celery_app

User = get_user_model()

from apps.general.outils.emailing import EmailingSystem
from apps.general.outils.notifications import NotificationSystem


@celery_app.task()
def enviar_email_task(newsletter, receiver_id, email_type):
    return EmailingSystem().enviar_email(newsletter, receiver_id, email_type)


@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().notify(object_related, notif_type)
    

@celery_app.task()
def check_programmed_newsletters_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            return enviar_email_task.delay()


@celery_app.task()
def share_social_media_content_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            return enviar_email_task.delay()