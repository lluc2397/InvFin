from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.general.tasks import enviar_email_task
from config import celery_app

from .models import WebsiteEmail

User = get_user_model()


@celery_app.task()
def send_website_email_task():
    for email_to_send in WebsiteEmail.objects.filter(sent = False):
        if email_to_send.date_to_send <= timezone.now():
            for user in User.objects.all():
                enviar_email_task.delay(email_to_send.for_task, user.id, 'web')
            email_to_send.sent = True
            email_to_send.save()
