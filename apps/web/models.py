from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    SET_NULL
)
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

from apps.emailing.models import Newsletter

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
        verbose_name = "Emails by website"
        db_table = "website_emails_type"


class WebsiteEmail(Newsletter):
    type_related = ForeignKey(WebsiteEmailsType, null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['-id']
        verbose_name = "Emails by website"
        db_table = "website_emails"
    