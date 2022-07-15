from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    TextField,
)
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()

from ckeditor.fields import RichTextField

from apps.general.mixins import BaseEscritosMixins, CommonMixin


class BaseWrittenContent(CommonMixin):
    title = CharField(max_length=500,null = True, blank=True)
    slug = CharField(max_length=500,null = True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    total_votes = IntegerField(default=0)
    total_views = PositiveIntegerField(default=0)
    times_shared = PositiveIntegerField(default=0)    
    category = ForeignKey("general.Category", on_delete=SET_NULL, blank=True, null=True)
    tags = ManyToManyField("general.Tag", blank=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def add_tags(self, tags):
        from apps.general.models import Tag
        for tag in tags:
            if tag == '':
                continue
            tag, created = Tag.objects.get_or_create(slug = tag.lower())
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


class BaseEscrito(BaseWrittenContent, BaseEscritosMixins):
    STATUS = ((1, 'Publicado'), (2, 'Borrador'), (3, 'Programado'), (4, 'Necesita revisión'))

    resume = TextField(default='')
    published_at = DateTimeField(auto_now=True)    
    status = IntegerField(null=True, blank=True,choices=STATUS)
    # thumbnail = CloudinaryField('image', null=True, width_field='image_width', height_field='image_height')
    thumbnail = ImageField('image',blank=True, null=True, width_field='image_width', height_field='image_height')
    non_thumbnail_url = CharField(max_length=500,null=True, blank=True)
    in_text_image = BooleanField(default=False)
    meta_information = ForeignKey("seo.MetaParametersHistorial", on_delete=SET_NULL, blank=True, null=True)

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

    def save(self, *args, **kwargs): # new
        return super().save(*args, **kwargs)        
        # return self.create_notification(self.id)

    def create_notification(self, id):
        pass


class BaseNewsletter(Model):
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


class BaseFavoritesHistorial(Model):
    user = ForeignKey(User,on_delete=SET_NULL,null=True, blank=True)
    date = DateTimeField(auto_now_add=True)
    added = BooleanField(default=False)
    removed = BooleanField(default=False)

    class Meta:
        abstract = True