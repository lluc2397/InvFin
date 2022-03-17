from config import celery_app

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.public_blog.models import PublicBlog, PublicBlogAsNewsletter, NewsletterFollowers


User = get_user_model()

from .utils import EmailingSystem, NotificationSystem

@celery_app.task()
def enviar_email_task(newsletter, receiver_id, email_type):
    EmailingSystem().enviar_email(newsletter, receiver_id, email_type)


@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().users_to_notify(object_related, notif_type)
    

@celery_app.task()
def check_programmed_newsletters_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            return enviar_email_task.delay()