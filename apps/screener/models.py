from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONField,
    ManyToManyField,
    Model,
    OneToOneField,
    SlugField,
    TextField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse

from apps.empresas.models import Company
from apps.etfs.models import Etf

User = get_user_model()

from apps.general.bases import BaseFavoritesHistorial
from apps.general.models import Category, Tag

from . import constants


class CompanyInformationBought(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Acción comprada"
        verbose_name_plural = "Acciones compradas"
        db_table = "favorites_stocks_boughts"

    def __str__(self):
        return f'{self.user.username} - {self.asset.name} - {self.id}'


class FavoritesStocksHistorial(BaseFavoritesHistorial):
    asset = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Acción favorita"
        verbose_name_plural = "Acción favoritas"
        db_table = "favorites_stocks_historial"

    def __str__(self):
        return f'{self.user.username} - {self.asset.name} - {self.id}'


class FavoritesStocksList(Model):
    user = OneToOneField(User,on_delete=SET_NULL,null=True, blank=True, related_name="favorites_companies")
    stock = ManyToManyField(Company, blank=True)

    class Meta:
        verbose_name = "Lista de acciones favoritas"
        verbose_name_plural = "Lista de acciones favoritas"
        db_table = "favorites_stocks_list"

    def __str__(self):
        return self.user.username


class FavoritesEtfsHistorial(BaseFavoritesHistorial):
    asset = ForeignKey(Etf, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "ETF favorito"
        verbose_name_plural = "ETF favoritos"
        db_table = "favorites_etfs_historial"

    def __str__(self):
        return f'{self.user.username} - {self.asset.name} - {self.id}'


class FavoritesEtfsList(Model):
    user = OneToOneField(User,on_delete=SET_NULL,null=True, blank=True)
    etf = ManyToManyField(Etf, blank=True)

    class Meta:
        verbose_name = "Lista de ETF favoritas"
        verbose_name_plural = "Lista de ETF favoritas"
        db_table = "favorites_etfs_list"

    def __str__(self):
        return self.user.username


class BasePrediction(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    date = DateTimeField(auto_now_add=True)
    optimistic_growth = FloatField(null=True, blank=True)
    neutral_growth = FloatField(null=True, blank=True)
    pesimistic_growth = FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class UserScreenerSimplePrediction(BasePrediction):
    class Meta:
        verbose_name = "Predicciones de los usuarios"
        verbose_name_plural = "Predicciones de los usuarios"
        db_table = "users_screener_simple_predictions"

    def __str__(self):
        return self.user.username + ' ' +self.company.ticker + ' ' + str(self.date)


class UserScreenerMediumPrediction(BasePrediction):
    optimistic_margin = FloatField(null=True, blank=True)
    neutral_margin = FloatField(null=True, blank=True)
    pesimistic_margin = FloatField(null=True, blank=True)
    optimistic_buyback = FloatField(null=True, blank=True)
    neutral_buyback = FloatField(null=True, blank=True)
    pesimistic_buyback = FloatField(null=True, blank=True)
    optimistic_fcf_margin = FloatField(null=True, blank=True)
    neutral_fcf_margin = FloatField(null=True, blank=True)
    pesimistic_fcf_margin = FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Predicciones elaboradas de los usuarios"
        db_table = "users_screener_medium_predictions"

    def __str__(self):
        return self.user.username + ' ' +self.company.ticker + ' ' + str(self.date)


class UserCompanyObservation(Model):
    STATUS = ((1, 'Fuerza'), (2, 'Oportunidad'), (3, 'Debilidad'), (4, 'Amenaza'))

    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True, related_name="company_foda")
    date = DateTimeField(auto_now_add=True)
    observation = RichTextField(default='', config_name='simple')
    observation_type = IntegerField(default=0, choices=STATUS)

    class Meta:
        verbose_name = "Observaciones sobre la empresa"
        db_table = "users_screener_companies_observations"

    def __str__(self):
        return self.user.username + ' ' +self.company.ticker + ' ' + str(self.date)
    
    def get_absolute_url(self):
        return reverse("screener:company", kwargs={"ticker": self.company.ticker})
    
    @property
    def observation_info(self):
        data = {}
        if self.observation_type == 1:
            data['status'] = 'Fuerza'
            data['color'] = 'info'
        elif self.observation_type == 2:
            data['status'] = 'Oportunidad'
            data['color'] = 'success'
        elif self.observation_type == 3:
            data['status'] = 'Debilidad'
            data['color'] = 'warning'
        else:
            data['status'] = 'Amenaza'
            data['color'] = 'danger'
        return data


class YahooScreener(Model):
    name = CharField(max_length=500)
    slug = SlugField(max_length=500)
    description = TextField()
    json_info = JSONField(default=dict)
    yq_name = CharField(max_length=500)
    asset_class_related = CharField(max_length=25, choices=constants.ASSET_CLASS)
    show = BooleanField(default=True)
    categories = ManyToManyField(Category, blank=True)
    tags = ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = "Yahoo screener"
        db_table = "screener_yahoo_screeners"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("screener:yahoo_screener", kwargs={"slug": self.slug})
