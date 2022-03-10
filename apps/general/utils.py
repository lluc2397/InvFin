from django.contrib.sites.models import Site

from apps.public_blog.models import (WritterProfile)

from .models import (
    Notification,
    NotificationsType
)

from django.contrib.auth import get_user_model
User = get_user_model()

class HostChecker:
    def __init__(self, request) -> None:
        self.request = request
        self.host = self.request.get_host().split('.')[0]
        self.current_domain = Site.objects.get_current().domain
    

    def check_writter(self):
        if WritterProfile.objects.filter(host_name = self.host).exists():
            return self.host
        else:
            return False
    
    def check_host(self):
        if self.host != self.current_domain and self.host != "www":
            return False
    
    def correct_host(self):
        if self.check_host() == False and self.check_writter == False:
            return f'http://{self.current_domain}'


class NotificationSystem:
    def __init__(self) -> None:
        self.new_blog_post = NotificationsType.objects.get_or_create(name = 'New blog post')[0]
        self.new_comment = NotificationsType.objects.get_or_create(name = 'New comment')[0]
        self.new_vote = NotificationsType.objects.get_or_create(name = 'New vote')[0]
        self.new_follower = NotificationsType.objects.get_or_create(name = 'New follower')[0]
        self.new_question = NotificationsType.objects.get_or_create(name = 'New question')[0]
        self.new_answer = NotificationsType.objects.get_or_create(name = 'New answer')[0]
        self.answer_accepted = NotificationsType.objects.get_or_create(name = 'Answer accepted')[0]

        """
        new_blog_post = 1
        new_comment = 2
        new_vote = 2
        new_follower = 3
        new_question = 4
        new_answer = 5
        answer_accepted = 6
        """
    

    def select_notification_type(self, notif_type_num):
        if notif_type_num == 1:
            notif_type = self.new_blog_post 
        elif notif_type_num == 2:
            notif_type = self.new_comment 
        elif notif_type_num == 2:
            notif_type = self.new_vote 
        elif notif_type_num == 3:
            notif_type = self.new_follower 
        elif notif_type_num == 4:
            notif_type = self.new_question 
        elif notif_type_num == 5:
            notif_type = self.new_answer 
        elif notif_type_num == 6:
            notif_type = self.answer_accepted 
        return notif_type


    def create_notif(self, user, object_related, notif_type):
        notif_type = self.select_notification_type(notif_type)

        notification =Notification.objects.create(
        user = user,
        object = object_related,
        notification_type = notif_type,
        )
        return notification
    

    def users_to_notify(self, object_related, notif_type):
        for user in User.objects.all():
            self.create_notif(user, object_related, notif_type)
        

        
