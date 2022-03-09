from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateField,
    BooleanField,
    PositiveIntegerField,
    FloatField,
    IntegerField,
    ManyToManyField
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
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify((self.name))
        return super().save(*args, **kwargs)


class Period(Model):    
    year = DateField()
    quarter = IntegerField(default=1)
    current_period = BooleanField(default=False)
    


class SuperinvestorHolding(Model):
    superinvestor_related = ForeignKey(Superinvestor, on_delete=SET_NULL, null=True, blank=True)
    period_related = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    percentage = FloatField(null=True, blank=True)
    num_shares = FloatField(null=True, blank=True)
    reported_price = FloatField(null=True, blank=True)

    @property
    def total_value(self):
        return self.num_shares * self.reported_price

    def __str__(self):
        texto = f'{self.superinvestor_related.name} - {self.company.ticker}'
        return texto
        



class SuperinvestorActivity(Model):
    MOVE = ((1, 'Compra'), (2, 'Venta'))

    superinvestor_related = ForeignKey(Superinvestor, on_delete=SET_NULL, null=True, blank=True)
    period_related = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    percentage_added = FloatField(null=True, blank=True)
    share_change = FloatField(null=True, blank=True)
    portfolio_change = FloatField(null=True, blank=True)
    is_new = BooleanField(default=False)
    movement = PositiveIntegerField(choices=MOVE)