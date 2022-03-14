from config import celery_app

from apps.general.utils import NotificationSystem

@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().users_to_notify(object_related, notif_type)


@celery_app.task()
def update_general_content_task(object_related, notif_type):
    return NotificationSystem().users_to_notify(object_related, notif_type)