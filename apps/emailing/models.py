from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    OneToOneField,
    DateTimeField,
    BooleanField,
    PositiveIntegerField,
    ManyToManyField
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.serializers import serialize
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.general.models import Notification


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


class NewsletterBaseDefaultField(Model):
    content = RichTextField(config_name='simple')
    times_used = PositiveIntegerField(default=0)
    in_use = BooleanField(default=True)
    date_created = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class NewsletterDefaultTitle(NewsletterBaseDefaultField):
    class Meta:
        ordering = ['times_used']
        verbose_name = "Default title"
        db_table = "newsletters_default_titles"

    def __str__(self):
        return self.content


class NewsletterDefaultIntroduction(NewsletterBaseDefaultField):
    class Meta:
        ordering = ['times_used']
        verbose_name = "Default intro"
        db_table = "newsletters_default_intro"

    def __str__(self):
        return self.content


class NewsletterDefaultDespedida(NewsletterBaseDefaultField):
    class Meta:
        ordering = ['times_used']
        verbose_name = "Default despedida"
        db_table = "newsletters_default_despedidas"

    def __str__(self):
        return self.content


class Newsletter(Model):
    use_default_title = BooleanField(default=False)
    use_default_introduction = BooleanField(default=False)
    use_default_despedida = BooleanField(default=False)
    title = CharField(max_length=99999)
    introduction = RichTextField(config_name='simple')
    despedida = RichTextField(config_name='simple')
    content = RichTextField(config_name='simple')
    default_title = ForeignKey(NewsletterDefaultTitle, on_delete=SET_NULL,blank=True, null=True)
    default_introduction = ForeignKey(NewsletterDefaultIntroduction, on_delete=SET_NULL,blank=True, null=True)
    default_despedida = ForeignKey(NewsletterDefaultDespedida, on_delete=SET_NULL,blank=True, null=True)
    sent = BooleanField(default=False)
    date_to_send = DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
    
    @property
    def app_label(self):
        return self._meta.app_label
    
    @property
    def object_name(self):
        return self._meta.object_name
    
    @property
    def for_task(self):
        to_json = self.__dict__
        to_json['app_label'] = self.app_label
        to_json['object_name'] = self.object_name
        to_json.pop('_state', None)
        return to_json


class WritterNewsletterDefaultOptions(Model):
    writter = OneToOneField(User, on_delete=CASCADE, blank=True, related_name='writter_default_options')
    default_titles = ManyToManyField(NewsletterDefaultTitle ,blank=True) 
    default_introductions = ManyToManyField(NewsletterDefaultIntroduction ,blank=True)
    default_despedidas = ManyToManyField(NewsletterDefaultDespedida ,blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Opciones por defecto"
        db_table = "newsletters_default_options"

    def __str__(self):
        return str(self.writter.username)
    
    @property
    def writter_has_default_options(self):
        return self.default_titles.exists()


class BaseEmail(Model):
    sent_to = ForeignKey(User, on_delete=CASCADE)
    date_sent = DateTimeField(auto_now_add=True)
    opened = BooleanField(default=False)
    date_opened = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
    
    @property
    def app_label(self):
        return self._meta.app_label
    
    @property
    def object_name(self):
        return self._meta.object_name
    
    @property
    def encoded_url(self):
        url = f'{self.id}-{self.app_label}-{self.object_name}'
        url = urlsafe_base64_encode(force_bytes(url))
        return url
        

class EmailNotification(BaseEmail):
    email_related = ForeignKey(Notification, null=True, blank=True, on_delete=SET_NULL, related_name = "email_related")

    class Meta:
        verbose_name = "Email from notifications"
        db_table = "emails_notifications"





