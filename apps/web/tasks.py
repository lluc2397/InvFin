from config import celery_app

from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.emailing.tasks import enviar_email_task
User = get_user_model()


@celery_app.task()
def send_website_email_task(newsletter):
    for user in User.objects.all()[:2]:
        enviar_email_task.delay(newsletter, user.id)
    return 