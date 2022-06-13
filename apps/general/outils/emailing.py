from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()


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