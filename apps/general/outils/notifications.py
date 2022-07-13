import time

from django.apps import apps
from django.contrib.auth import get_user_model

from .. import constants as NotificationsType
from ..models import Notification

User = get_user_model()


class NotificationSystem:
  
    """
    new_blog_post    -----> followers
    new_comment      -----> related
    new_vote         -----> single
    new_follower     -----> sinlge
    new_question     -----> all
    new_answer       -----> related
    answer_accepted  -----> related
    purchase_successful-----> sinlge
    """  

    def save_notif(self, user, object_related, notif_type_num):
        from ..tasks import enviar_email_task
        notif_type = self.select_notification_type(notif_type_num)

        notification = Notification.objects.create(
        user = user,
        object = object_related,
        notification_type = notif_type,
        )
        email = {
            'subject': object_related.title,
            'content': object_related.content,
            'url_to_join': object_related.shareable_link,
            'app_label': notification.app_label,
            'object_name': notification.object_name,
            'id': notification.pk
        }
        return enviar_email_task.delay(email, user.pk, 'notif')

    def notify_related_users(self, question, notif_type_num):
        pass

    def notify_all_users(self, object_related, notif_type_num):
        for user in User.objects.all():
            self.save_notif(user, object_related, notif_type_num)

    def notify_all_followers(self, object_related, notif_type_num):
        for user in object_related.author.main_writter_followed.followers.all():
            self.save_notif(user, object_related, notif_type_num)

    def notify_single_user(self, user, object_related, notif_type_num):
        self.save_notif(user, object_related, notif_type_num)            

    def notify(self, object_related, notif_type:str):
        """
        whom_notify may be all, followers or single
        """
        time.sleep(10)
        app_label = object_related['app_label']
        object_name = object_related['object_name']
        id = object_related['id']

        object_related = apps.get_model(app_label, object_name, require_ready=True).objects.get(pk=id)

        if notif_type_num == 1:
            self.notify_all_followers(object_related, notif_type_num)

        elif notif_type_num == 2 or notif_type_num == 6 or notif_type_num == 7:
            self.notify_related_users(object_related, notif_type_num)

        elif notif_type_num == 3 or notif_type_num == 4:
            self.notify_single_user(object_related, notif_type_num)

        elif notif_type_num == 5:
            self.notify_all_users(object_related, notif_type_num)