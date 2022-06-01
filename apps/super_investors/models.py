from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    DateTimeField,
    DateField,
    BooleanField,
    PositiveIntegerField,
    FloatField,
    IntegerField,
    TextField
)

from apps.empresas.models import Company

from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
MyUser = get_user_model()


class Superinvestor(Model):
    name = CharField(max_length=600000, null=True, blank=True)
    fund_name = CharField(max_length=600000, null=True, blank=True)
    info_accronym = CharField(max_length=600000, null=True, blank=True)
    slug = CharField(max_length=600000, null=True, blank=True)
    last_update = DateTimeField(null=True, blank=True)
    has_error = BooleanField(default=False)
    error = TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Superinvestor"
        verbose_name_plural = "Superinvestors"
        db_table = "superinvestors"
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify((self.name))
        return super().save(*args, **kwargs)


class Period(Model):
    PERIODS = ((1, '1 Quarter'), (2, '2 Quarter'), (3, '3 Quarter'), (4, '4 Quarter'))
    year = DateField(null=True, blank=True)
    period = IntegerField(choices=PERIODS, null=True, blank=True)

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        db_table = "assets_periods"
    
    def __str__(self):
        return str(self.year)     


class SuperinvestorActivity(Model):
    MOVE = ((1, 'Compra'), (2, 'Venta'))

    superinvestor_related = ForeignKey(Superinvestor, on_delete=SET_NULL, null=True, blank=True)
    period_related = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    percentage_share_change = FloatField(null=True, blank=True)
    share_change = FloatField(null=True, blank=True)
    portfolio_change = FloatField(null=True, blank=True)
    is_new = BooleanField(default=False)
    movement = PositiveIntegerField(choices=MOVE)
    company_name = TextField(blank=True, null=True)
    not_registered_company = BooleanField(default=False)
    need_verify_company = BooleanField(default=False)

    class Meta:
        verbose_name = "Superinvestor activity"
        verbose_name_plural = "Superinvestors activity"
        db_table = "superinvestors_activity"