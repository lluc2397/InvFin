# send_mail('subject', 'message', 'Dont Reply <do_not_reply@domain.com>', ['youremail@example.com'])
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

EMAIL_CONTACT = settings.EMAIL_CONTACT
EMAIL_NEWSLETTER = settings.EMAIL_NEWSLETTER
MAIN_EMAIL = settings.MAIN_EMAIL
EMAIL_ACCOUNTS = settings.EMAIL_ACCOUNTS

def send_email():
    pass


def create_email(title, sender, receiver, ref, tu_or_hay, tema, action):

    message = render_to_string('general/emailing/newsletter.html', {
        'usuario': user_to_notify,
        'introduction':introduction,
        'content':content,
        'despedida':despedida,
        'image_tag':image_tag
    })
    
    email_message = EmailMessage(
        title, 
        message,
        f"{sender} <{email_used}>",
        [receiver.email]
    )
    
    email_message.content_subtype = "html"
    email_message.send()