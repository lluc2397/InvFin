from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

import binascii
import os
import time
import csv

from apps.public_blog.models import WritterProfile

from .models import (
    Notification,
    NotificationsType
)

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
    def __init__(self) -> None:
        self.new_blog_post = NotificationsType.objects.get_or_create(name = 'Nuevo escrito')[0]
        self.new_comment = NotificationsType.objects.get_or_create(name = 'Nuevo comentario')[0]
        self.new_vote = NotificationsType.objects.get_or_create(name = 'Nuevo voto')[0]
        self.new_follower = NotificationsType.objects.get_or_create(name = 'Nuevo seguidor')[0]
        self.new_question = NotificationsType.objects.get_or_create(name = 'Nueva pregunta')[0]
        self.new_answer = NotificationsType.objects.get_or_create(name = 'Nueva respuesta')[0]
        self.answer_accepted = NotificationsType.objects.get_or_create(name = 'Respuesta acceptada')[0]

        """
        new_blog_post = 1    -----> followers
        new_comment = 2      -----> related
        new_vote = 3         -----> single
        new_follower = 4     -----> sinlge
        new_question = 5     -----> all
        new_answer = 6       -----> related
        answer_accepted = 7  -----> related
        """  

    def select_notification_type(self, notif_type_num):
        if notif_type_num == 1:
            notif_type = self.new_blog_post
        elif notif_type_num == 2:
            notif_type = self.new_comment 
        elif notif_type_num == 3:
            notif_type = self.new_vote 
        elif notif_type_num == 4:
            notif_type = self.new_follower 
        elif notif_type_num == 5:
            notif_type = self.new_question 
        elif notif_type_num == 6:
            notif_type = self.new_answer 
        elif notif_type_num == 7:
            notif_type = self.answer_accepted 
        return notif_type

    def save_notif(self, user, object_related, notif_type_num):
        from .tasks import enviar_email_task
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

    def notify(self, object_related, notif_type_num:int):
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
      

class ExportCsv:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        meta = f'{meta}'.replace('.', '-')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to csv"


class UniqueCreator:
    @classmethod
    def create_unique_field(cls, model, value, field, original_value=None, extra:int = 0):
        if model.__class__.objects.filter(**{field:value}).exists():
            if field == 'key':
                value = UniqueCreator.generate_key()
            else:
                value = UniqueCreator.generate_slug(original_value, extra)
            return UniqueCreator.create_unique_field(value, field)
        return value
    
    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
    
    @classmethod
    def generate_slug(cls, value=None, extra:int = 0):
        extra += 1
        return slugify(value + str(extra))