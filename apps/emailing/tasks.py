from config import celery_app
from .utils import EmailingSystem

@celery_app.task()
def enviar_email_task(newsletter, receiver_id, email_type):
    EmailingSystem().enviar_email(newsletter, receiver_id, email_type)
