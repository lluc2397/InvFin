from datetime import datetime, timedelta, time

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
    Q
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.escritos.models import Term
from apps.empresas.models import Company

from .managers import KeyManager


User = get_user_model()


class Key(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name="api_key")
    ip = CharField(max_length=50, null=True, blank=True)
    key = CharField(_("Key"), max_length=40, primary_key=True)
    in_use = BooleanField(default=True)
    created = DateTimeField(_("Created"), auto_now_add=True)
    removed = DateTimeField(_("Removed"), blank=True)
    limit = PositiveIntegerField(default=0)
    objects = KeyManager()

    class Meta:
        verbose_name = "Key"
        verbose_name_plural = "Keys"
        db_table = "api_keys"

    def save(self, *args, **kwargs):
        if not self.key:
            key = KeyManager.generate_key()
            self.key = KeyManager.create_unique_field(key, self.key)
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

    