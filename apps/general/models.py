from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    IntegerField,
    BooleanField,
)

from django.template.defaultfilters import slugify

from cloudinary.models import CloudinaryField

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.general.bases import BaseEmail, BaseGenericModels


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


class Country(Model):
    country = CharField(max_length=500 , null=True, blank=True)
    iso = CharField(max_length=500 , null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "assets_countries"

    def __str__(self):
        return str(self.country)


class Currency(Model):
    currency = CharField(max_length=500 , null=True, blank=True)
    symbol = CharField(max_length=5, null=True, blank=True)
    name = CharField(max_length=500 , null=True, blank=True)
    iso = CharField(max_length=500 , null=True, blank=True)
    decimals = IntegerField(default=2, blank=True)
    country = ForeignKey(Country,
        on_delete=CASCADE,
        null=True,
        related_name = "currency"
    )

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        db_table = "assets_currencies"

    def __str__(self):
        return str(self.currency)


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
        

class EmailNotification(BaseEmail):
    email_related = ForeignKey(Notification, null=True, blank=True, on_delete=SET_NULL, related_name = "email_related")

    class Meta:
        verbose_name = "Email from notifications"
        db_table = "emails_notifications"
