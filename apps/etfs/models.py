from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    FloatField,
    ForeignKey,
    PositiveBigIntegerField,
    DateField
)

from apps.empresas.models import Company, Exchange

class Etf(Model):
    ticker = CharField(max_length=6000000)
    name = CharField(max_length=600000)
    exchange = ForeignKey(Exchange, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "ETF"
        verbose_name_plural = "ETFs"
        db_table = "etfs"

    def __str__(self):
        return str(self.ticker)


class EtfComposition(Model):
    etf_related = ForeignKey(Etf, on_delete=SET_NULL, null=True, blank=True)
    date = DateField(null=True, blank=True)
    company_related = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    company_size = FloatField(null=True, blank=True)
    number_shares = PositiveBigIntegerField(default=0,null=True, blank=True)

    class Meta:
        verbose_name = "ETF composition"
        verbose_name_plural = "ETFs composition"
        db_table = "etfs_composition"

    def __str__(self):
        return str(self.etf_related.ticker)
