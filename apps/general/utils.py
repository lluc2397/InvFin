from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model

import time

from apps.public_blog.models import WritterProfile

from .models import Notification
from .constants import NOTIFICATIONS_TYPES

User = get_user_model()


class ChartSerializer:
    def generate_json(self, comparing_json:dict, items:list=None, chart_type:str='line')->dict:
        labels = comparing_json['labels']
        chartData = {
            'labels': labels,
            'fields': []
        }
        if not items:
            items = [i for i in range(len(comparing_json['fields']))]

        fields_for_chart = [comparing_json['fields'][num] for num in items]

        for field in fields_for_chart:
            comparaison_dict = {
                    'label': field['title'],
                    'data': field['values'],
                    'backgroundColor': '',
                        'borderColor': '',
                    
                    'yAxisID':"right",
                    'order': 0,
                    'type': chart_type
            }
            chartData['fields'].append(comparaison_dict)
        
        return chartData


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


class EmailingSystem():
    def __init__(self) -> None:
        self.newsletter_template = 'general/emailing/newsletter.html'
        self.notification_template = 'general/emailing/notification.html'
        self.web_template = 'general/emailing/web.html'

        self.email_contacto = settings.EMAIL_CONTACT
        self.email_newsletter = settings.EMAIL_NEWSLETTER
        self.email_lucas = settings.MAIN_EMAIL
        self.email_cuentas = settings.EMAIL_ACCOUNTS
        self.email_no_responder = settings.EMAIL_DEFAULT
    

    def simple_email(self, message):
        subject = 'Nuevo mensaje desde suport'
        return send_mail(subject, message, self.email_no_responder, [self.email_no_responder])


    def prepare_email_track(self, email_content, receiver):        
        app_label, object_name, email_id = email_content['app_label'], email_content['object_name'], email_content['id']
        email_modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(pk = email_id)
        email_track = email_modelo.email_related.create(sent_to = receiver)
        image_tag = email_track.encoded_url
        return image_tag
    

    def prepare_web_email(self, email_content, receiver, image_tag):
        subject = email_content['title']
        content = email_content['content']

        message = render_to_string(self.web_template, {
            'usuario': receiver,
            'content':content,
            'image_tag':image_tag
        })

        sender = f"Lucas - InvFin <{self.email_lucas}>"

        return subject, message, sender

    def prepare_newsletter(self, email_content, receiver, image_tag):

        subject = email_content['title']
        introduction = email_content['introduction']
        content = email_content['content']
        despedida = email_content['despedida']
        
        message = render_to_string(self.newsletter_template, {
            'usuario': receiver,
            'introduction':introduction,
            'content':content,
            'despedida':despedida,
            'image_tag':image_tag
        })

        sender = f"{sender} <{self.email_newsletter}>"
        
        return subject, message, sender


    def prepare_email_notifications(self, email_content, receiver, image_tag):
        subject = email_content['subject']
        content = email_content['content']
        url_to_join = email_content['url_to_join']

        message = render_to_string(self.newsletter_template, {
            'usuario': receiver,
            'content':content,
            'url_to_join':url_to_join,
            'image_tag':image_tag
        })

        sender = f"InvFin Notificaciones <{self.email_no_responder}>"

        return subject, message, sender


    def enviar_email(self, email, receiver_id, email_type):
        """
        email_type may be news, notif or web
        """

        receiver = User.objects.get(id = receiver_id)
        image_tag = self.prepare_email_track(email, receiver)

        if email_type == 'notif':
            subject, message, sender = self.prepare_email_notifications(email, receiver, image_tag)
        elif email_type == 'web':
            subject, message, sender = self.prepare_web_email(email, receiver, image_tag)
        elif email_type == 'news':
            subject, message, sender = self.prepare_newsletter(email, receiver, image_tag)
        
        email_message = EmailMessage(
            subject, 
            message,
            sender,
            [receiver.email]
        )
        
        email_message.content_subtype = "html"
        email_message.send()


class NotificationSystem:
    """
    new_blog_post = 1    -----> followers
    new_comment = 2      -----> related
    new_vote = 3         -----> single
    new_follower = 4     -----> sinlge
    new_question = 5     -----> all
    new_answer = 6       -----> related
    answer_accepted = 7  -----> related
    new_obs_company = 8  -----> related
    new_news_company = 9  -----> related
    """  

    def save_notif(self, user, object_related, notif_type):
        from .tasks import enviar_email_task

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

    def notify_related_users(self, object_name:str, object_related, notif_type:str, attr:str):
        for obj in object_related.related_users:
            if object_name == 'question':
                user = obj.author
            else:
                user = obj.user
            user_profile = user.user_profile
            field = getattr(user_profile, attr)
            if field and user_profile.field is True:
                self.save_notif(user, object_related, notif_type)

    def notify_all_users(self, object_related, notif_type):
        for user in User.objects.all():
            self.save_notif(user, object_related, notif_type)

    def notify_all_followers(self, object_related, notif_type):
        for user in object_related.author.main_writter_followed.followers.all():
            self.save_notif(user, object_related, notif_type)

    def notify_single_user(self, user, object_related, notif_type):
        self.save_notif(user, object_related, notif_type)            

    def notify(self, object_related:dict, whom_notify:str, notif_type:str, attr:str):
        """
        whom_notify may be all, relateds or single
        """
        app_label = object_related['app_label']
        object_name = object_related['object_name']
        id = object_related['id']

        object_related = apps.get_model(app_label, object_name, require_ready=True).objects.get(pk=id)

        if whom_notify == 'all':
            self.notify_all_followers(object_related, notif_type)

        elif whom_notify == 'relateds':
            self.notify_related_users(object_name, object_related, notif_type, attr)

        else:
            self.notify_single_user()        
