from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
User = get_user_model()


EMAIL_CONTACT = settings.EMAIL_CONTACT
EMAIL_NEWSLETTER = settings.EMAIL_NEWSLETTER
MAIN_EMAIL = settings.MAIN_EMAIL
EMAIL_ACCOUNTS = settings.EMAIL_ACCOUNTS


def create_email_track(app_label, object_name, newsletter_id, receiver):
    modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id = newsletter_id)
    email_modelo = modelo.email_related.create(sent_to = receiver)
    return email_modelo


def enviar_email(newsletter, receiver_id):
    sender = 'Lucas'

    receiver = User.objects.get(id = receiver_id)
    app_label, object_name, newsletter_id = newsletter['app_label'], newsletter['object_name'], newsletter['id']
    email_track = create_email_track(app_label, object_name, newsletter_id, receiver)
    image_tag = email_track.encoded_url

    title = newsletter['title']
    introduction = newsletter['introduction']
    content = newsletter['content']
    despedida = newsletter['despedida']

    
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
        f"{sender} <{EMAIL_NEWSLETTER}>",
        [receiver.email]
    )
    
    email_message.content_subtype = "html"
    email_message.send()