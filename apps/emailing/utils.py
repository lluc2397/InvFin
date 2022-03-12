from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()


EMAIL_CONTACT = settings.EMAIL_CONTACT
EMAIL_NEWSLETTER = settings.EMAIL_NEWSLETTER
MAIN_EMAIL = settings.MAIN_EMAIL
EMAIL_ACCOUNTS = settings.EMAIL_ACCOUNTS


def enviar_email(title, sender, receiver, ref, tu_or_hay, tema, action):
    image_tag = sent_to
    message = render_to_string('general/emailing/newsletter.html', {
        'usuario': receiver,
        'introduction':introduction,
        'content':content,
        'despedida':despedida,
        'image_tag':image_tag
    })
    
    email_message = EmailMessage(
        title, 
        message,
        f"{sender.full_name} <{EMAIL_NEWSLETTER}>",
        [receiver.email]
    )
    
    email_message.content_subtype = "html"
    email_message.send()