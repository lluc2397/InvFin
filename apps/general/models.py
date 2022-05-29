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
    ManyToManyField,
    SlugField
)

from django.contrib.sitemaps import ping_google
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cloudinary.models import CloudinaryField

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.seo.models import MetaParametersHistorial

from .mixins import CommonMixin, BaseEscritosMixins


class EscritosClassification(Model):
    name = CharField(max_length=500,null = True, blank=True, unique = True)
    slug = CharField(max_length=500,null = True, blank=True, unique = True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(EscritosClassification):
    class Meta:
        verbose_name = "Category"
        db_table = "categories"


class Tag(EscritosClassification):
    class Meta:
        verbose_name = "Tag"
        db_table = "tags"


class BasicWrittenContent(CommonMixin):
    title = CharField(max_length=1000, null=True, blank=True)
    slug = SlugField(max_length=1000, null=True, blank=True, unique=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    total_votes = IntegerField(default=0)
    total_views = PositiveIntegerField(default=0)
    times_shared = PositiveIntegerField(default=0)    
    category = ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True)
    tags = ManyToManyField(Tag, blank=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        from .utils import UniqueCreator
        if not self.slug:
            slug = UniqueCreator.create_unique_field(
                self, 
                slugify(self.title),
                'slug',
                self.title
            )
            self.slug = slug
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def add_tags(self, tags):
        for tag in tags:
            if tag == '':
                continue
            exist_tag = Tag.objects.filter(name = tag.lower())
            if exist_tag.exists():
                tag = exist_tag[0]                
            else:
                tag = Tag.objects.create(name = tag.lower())
            
            if tag in self.tags.all():
                continue
            self.tags.add(tag)
    
    @property
    def shareable_link(self):        
        try:
            url = self.custom_url
        except:
            slug = self.get_absolute_url()
            url = f"https://inversionesyfinanzas.xyz{slug}"
        return url


class BaseEscrito(BasicWrittenContent, BaseEscritosMixins):
    STATUS = ((1, 'Publicado'), (2, 'Borrador'), (3, 'Programado'), (4, 'Necesita revisión'))

    resume = TextField(default='')
    published_at = DateTimeField(auto_now=True)    
    status = IntegerField(null=True, blank=True,choices=STATUS)
    # thumbnail = CloudinaryField('image', null=True, width_field='image_width', height_field='image_height')
    thumbnail = ImageField('image',blank=True, null=True, width_field='image_width', height_field='image_height')
    non_thumbnail_url = CharField(max_length=500,null=True, blank=True)
    in_text_image = BooleanField(default=False)
    meta_information = ForeignKey(MetaParametersHistorial, on_delete=SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs): # new
        return super().save(*args, **kwargs)
    
    @property
    def image(self):
        image = self.non_thumbnail_url
        if self.thumbnail:
            image = self.thumbnail.url
        if not image:
            image = '/static/general/assets/img/general/why-us.webp'
        return image
    
    
class BaseComment(Model):
    author = ForeignKey(User, on_delete=SET_NULL, null=True) 
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Industry(Model):
    industry = CharField(max_length=500, null=True, blank=True)
    industry_spanish = CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        db_table = "assets_industries"

    def __str__(self):
        return str(self.industry)


class Sector(Model):
    sector = CharField(max_length=500 , null=True, blank=True)
    sector_spanish = CharField(max_length=500 , null=True, blank=True)

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        db_table = "assets_sectors"

    def __str__(self):
        return str(self.sector)


class Currency(Model):
    currency = CharField(max_length=500 , null=True, blank=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        db_table = "assets_currencies"

    def __str__(self):
        return str(self.currency)


class Country(Model):
    country = CharField(max_length=500 , null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "assets_countries"

    def __str__(self):
        return str(self.country)


class BaseGenericModels(Model):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    def __str__(self, *args, **kwargs):
        return str(self.id)
    
    @property
    def app_label(self):
        return self._meta.app_label
    
    @property
    def object_name(self):
        return self._meta.object_name


class NotificationsType(Model):
    name = CharField(max_length=500)

    class Meta:
        verbose_name = "Notification type"
        db_table = "notifications_types"

    def __str__(self, *args, **kwargs):
        return self.name


class Notification(BaseGenericModels):
    user = ForeignKey(User, on_delete=CASCADE)
    notification_type = ForeignKey(NotificationsType, on_delete=CASCADE)
    is_seen = BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        db_table = "notifications"


class FavoritesHistorial(Model):
    user = ForeignKey(User,on_delete=SET_NULL,null=True, blank=True)
    date = DateTimeField(auto_now_add=True)
    added = BooleanField(default=False)
    removed = BooleanField(default=False)

    class Meta:
        abstract = True


class Newsletter(Model):
    title = CharField(max_length=500)
    content = RichTextField(config_name='simple')
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
        to_json = {
            'app_label': self.app_label,
            'object_name': self.object_name,
            'title': self.title,
            'content': self.content,
            'id': self.pk,
        }        
        return to_json


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
