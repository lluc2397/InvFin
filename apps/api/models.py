from django.conf import settings
from datetime import datetime, timedelta, time
from django.template.defaultfilters import slugify
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
    Q,
    JSONField,
    IntegerField
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.escritos.models import Term
from apps.empresas.models import Company
from apps.general.utils import UniqueCreator

from .managers import KeyManager


User = get_user_model()
API_version = settings.API_VERSION['CURRENT_VERSION']

class Key(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name="api_key")
    ip = CharField(max_length=50, null=True, blank=True)
    key = CharField(_("Key"), max_length=40, primary_key=True)
    in_use = BooleanField(default=True)
    created = DateTimeField(_("Created"), auto_now_add=True)
    removed = DateTimeField(_("Removed"), null=True, blank=True)
    limit = PositiveIntegerField(default=0)
    objects = KeyManager()

    class Meta:
        verbose_name = "Key"
        verbose_name_plural = "Keys"
        db_table = "api_keys"
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.key:
            key = UniqueCreator.create_unique_field(
                self,
                UniqueCreator.generate_key(),
                'key'    
            )
            self.key = key
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.key


class ReasonKeyRequested(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    created = DateTimeField(_("Created"), auto_now_add=True)
    description = TextField()

    class Meta:
        verbose_name = "Reason for requesting Key"
        verbose_name_plural = "Reason for requesting Key"
        db_table = "api_reason_key"


class BaseRequestAPI(Model):
    ip = CharField(max_length=50)
    key = ForeignKey(Key, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    date = DateTimeField(auto_now_add=True)
    path = CharField(max_length=500)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return f'{self.user} - {self.search}'
    
    @property
    def count_use_today(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        return self.objects.filter((Q(date__lte=today_start) & Q(date__gte=today_end)), key=self.key).count()


class CompanyRequestAPI(BaseRequestAPI):
    search = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    is_excel = BooleanField(default=False)

    class Meta:
        verbose_name = "Company requested"
        verbose_name_plural = "Companies requested"
        db_table = "api_companies_requested"


class TermRequestAPI(BaseRequestAPI):
    search = ForeignKey(Term, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Term requested"
        verbose_name_plural = "Terms requested"
        db_table = "api_terms_requested"


class EndpointsCategory(Model):
    title = CharField(max_length=250)

    class Meta:
        verbose_name = "Endpoints category"
        verbose_name_plural = "Endpoints categories"
        db_table = "api_endpoints_categories"


class Endpoint(Model):
    title_related = ForeignKey(EndpointsCategory, on_delete=SET_NULL, null=True, blank=True)
    title = CharField(max_length=250, blank=True)
    slug = CharField(max_length=250, blank=True)
    url = CharField(max_length=250, blank=True)
    description = TextField(blank=True)
    url_example = CharField(max_length=250, blank=True)
    response_example = JSONField(blank=True)    
    date_created = DateTimeField(auto_now_add=True)
    is_premium = BooleanField(default=False)
    is_available = BooleanField(default=True)
    is_deprecated = BooleanField(default=False)
    version = CharField(max_length=3, blank=True, default=API_version)
    date_deprecated = DateTimeField(blank=True)
    price = IntegerField(default=0)

    class Meta:
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"
        db_table = "api_endpoints"

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify((self.name))
        self.result_example = self.result_example.replace('<pre>','').replace('</pre>','')
        return super().save(*args, **kwargs)
    
    @property
    def final_url(self):
        return f'api/{self.version}/{self.url}'