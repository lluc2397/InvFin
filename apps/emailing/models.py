from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    PositiveIntegerField,
    ImageField,
    IntegerField,
    ManyToManyField
)
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
User = get_user_model()


from apps.general.models import Notification


class NewsletterDefaultTitle(Model):
    content = TextField()
    times_used = PositiveIntegerField(default=0)

    class Meta:
        ordering = ['times_used']
        verbose_name = "Default title"
        db_table = "newsletters_default_titles"

    def __str__(self):
        return self.content


class NewsletterDefaultIntroduction(Model):
    content = RichTextField(config_name='simple')
    times_used = PositiveIntegerField(default=0)

    class Meta:
        ordering = ['times_used']
        verbose_name = "Default intro"
        db_table = "newsletters_default_intro"

    def __str__(self):
        return self.content


class NewsletterDefaultDespedida(Model):
    content = RichTextField(config_name='simple')
    times_used = PositiveIntegerField(default=0)

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
    introduction = TextField()
    despedida = TextField()
    content = RichTextField()
    default_title = ForeignKey(NewsletterDefaultTitle, on_delete=SET_NULL, null=True)
    default_introduction = ForeignKey(NewsletterDefaultIntroduction, on_delete=SET_NULL, null=True)
    default_despedida = ForeignKey(NewsletterDefaultDespedida, on_delete=SET_NULL, null=True)
    sent = BooleanField(default=False)
    date_to_send = DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class WritterNewsletterDefaultOptions(Model):
    writter = ForeignKey(User, on_delete=CASCADE, blank=True)
    default_titles = ManyToManyField(NewsletterDefaultTitle ,blank=True) 
    default_introductions = ManyToManyField(NewsletterDefaultIntroduction ,blank=True)
    default_despedidas = ManyToManyField(NewsletterDefaultDespedida ,blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = "Opciones por defecto"
        db_table = "newsletters_default_options"

    def __str__(self):
        return str(self.writter.username)


class BaseEmail(Model):
    sent_to = ForeignKey(User, on_delete=CASCADE)
    date_sent = DateTimeField(auto_now_add=True)
    opened = BooleanField(default=False)
    date_opened = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class EmailNotification(BaseEmail):
    email_related = ForeignKey(Notification,null=True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Email from notifications"
        db_table = "emails_notifications"


class EmailPublicBlog(BaseEmail):
    email_related = ForeignKey('public_blog.PublicBlogAsNewsletter',null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Email from public blog"
        db_table = "emails_public_blog"


class EmailWebsite(BaseEmail):
    email_related = ForeignKey('web.WebsiteEmail',null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Email from public blog"
        db_table = "emails_website"