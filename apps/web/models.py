from ckeditor.fields import RichTextField
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    JSONField,
    ManyToManyField,
    Model,
    PositiveBigIntegerField,
    SlugField,
    TextField,
)
from django.template.defaultfilters import slugify

from apps.general.bases import BaseEmail, BaseNewsletter
from apps.seo.models import Visiteur
from apps.socialmedias.constants import SOCIAL_MEDIAS
from apps.seo import constants
from apps.users.models import User

class WebsiteLegalPage(Model):
    title = CharField(max_length=8000)
    slug = CharField(max_length=8000, null=True)
    content = RichTextField()

    class Meta:
        ordering = ['-id']
        verbose_name = "Legal website pages"
        db_table = "website_pages_legals"
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class WebsiteEmailsType(Model):
    name = CharField(max_length=8000)

    class Meta:
        ordering = ['-id']
        verbose_name = "Emails type by website"
        db_table = "website_emails_type"
    
    def __str__(self) -> str:
        return self.name


class WebsiteEmail(BaseNewsletter):
    type_related = ForeignKey(WebsiteEmailsType, null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['-id']
        verbose_name = "Emails by website"
        db_table = "website_emails"

    def __str__(self) -> str:
        return self.title
    
    @property
    def opening_rate(self):
        all_emails = self.email_related.all()
        all_opened = self.email_related.filter(opened=True).count()
        rate = all_emails / all_opened if all_opened != 0 else 0
        return rate


class WebsiteEmailTrack(BaseEmail):
    email_related = ForeignKey(WebsiteEmail, null = True, blank=True, on_delete=SET_NULL, related_name = "email_related")

    class Meta:
        verbose_name = "Email counting"
        db_table = "website_emails_track"
    
    def __str__(self) -> str:
        return self.email_related.title


class PromotionCampaign(Model):
    title = CharField(max_length=600, blank=True)
    slug = SlugField(blank=True)
    categories = ManyToManyField('general.Category', blank=True)
    tags = ManyToManyField('general.Tag', blank=True)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Promotions campaigns"
        db_table = "promotions_campaigns"

    def __str__(self) -> str:
        return self.title


class Promotion(Model):
    title = CharField(max_length=600, blank=True)
    content = RichTextField()
    thumbnail = CharField(max_length=600, blank=True)
    slug = SlugField()
    prize = PositiveBigIntegerField(default=0)
    has_prize = BooleanField(default=False)
    shareable_url = CharField(max_length=600, blank=True)
    redirect_to = CharField(max_length=600, blank=True)
    medium = CharField(max_length=250, choices=constants.MEDIUMS, blank=True)
    web_promotion_type = CharField(max_length=250, choices=constants.WEP_PROMOTION_TYPE, blank=True)
    web_location = CharField(max_length=250, choices=constants.WEP_PROMOTION_LOCATION, blank=True)
    web_place = CharField(max_length=250, choices=constants.WEP_PROMOTION_PLACE, blank=True)
    social_media = CharField(max_length=250, blank=True, choices=SOCIAL_MEDIAS)
    publication_date = DateTimeField(blank=True)
    campaign_related = ForeignKey(PromotionCampaign, on_delete=SET_NULL, null=True, blank=True)
    reuse = BooleanField(default=False)
    times_to_reuse = PositiveBigIntegerField(default=0)
    users_clicked = ManyToManyField(User, blank=True)
    visiteurs_clicked = ManyToManyField(Visiteur, blank=True)
    clicks_by_user = PositiveBigIntegerField(default=0)
    clicks_by_not_user = PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = "Promociones"
        db_table = "promotions"
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def full_url(self):
        source = 'invfin'
        if self.medium != source:            
            source = self.social_media
        utm_source = f'utm_source={source}'
        utm_medium = f'utm_medium={self.medium}'
        utm_campaign = f'utm_campaign={self.campaign_related.title}'
        utm_term = f'utm_term={self.title}'
        return f'{self.redirect_to}?{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'