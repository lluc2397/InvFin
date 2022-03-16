from config import celery_app

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.public_blog.models import PublicBlog, PublicBlogAsNewsletter, NewsletterFollowers
from apps.emailing.tasks import enviar_email_task

User = get_user_model()

from apps.general.utils import NotificationSystem



@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().users_to_notify(object_related, notif_type)
    

@celery_app.task()
def check_programmed_newsletters_task():
    for blog_newsletter in PublicBlogAsNewsletter.objects.filter(sent = False):
        if blog_newsletter.date_to_send <= timezone.now():
            return enviar_email_task.delay()