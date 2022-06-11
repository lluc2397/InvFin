from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    OneToOneField,
    ManyToManyField,
    ForeignKey,
    DateTimeField,
    DateField,
    BooleanField,
    PositiveIntegerField,
    FloatField,
    IntegerField,
    TextField
)
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model

from apps.empresas.models import Company
from apps.general.bases import BaseFavoritesHistorial

from .managers import SuperinvestorManager

User = get_user_model()


class Superinvestor(Model):
    name = CharField(max_length=600, null=True, blank=True)
    fund_name = CharField(max_length=600, null=True, blank=True)
    info_accronym = CharField(max_length=20, null=True, blank=True)
    slug = CharField(max_length=600, null=True, blank=True)
    last_update = DateTimeField(null=True, blank=True)
    has_error = BooleanField(default=False)
    error = TextField(blank=True, null=True)
    image = CharField(max_length=600, null=True, blank=True)
    objects = SuperinvestorManager()

    class Meta:
        verbose_name = "Superinvestor"
        verbose_name_plural = "Superinvestors"
        db_table = "superinvestors"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("super_investors:superinvestor", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify((self.name))
        return super().save(*args, **kwargs)
    
    @property
    def current_portfolio(self):
        last_period = Period.objects.latest()
        return self.history.filter(period_related=last_period)
        
    @property
    def total_number_of_holdings(self):
        return self.current_portfolio.count()
    
    @property
    def portfolio_value(self):
        return sum(position.total_value for position in self.current_portfolio)

    @property
    def top_holdings(self):
        return self.current_portfolio.order_by('portfolio_weight')[:5]


class FavoritesSuperinvestorsHistorial(BaseFavoritesHistorial):
    superinvestor = ForeignKey(Superinvestor, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Superinvestor favorita"
        verbose_name_plural = "Superinvestor favoritas"
        db_table = "favorites_superinvestor_historial"

    def __str__(self):
        return f'{self.id}'


class FavoritesSuperinvestorsList(Model):
    user = OneToOneField(User,on_delete=SET_NULL,null=True, blank=True, related_name="favorites_superinvestors")
    superinvestor = ManyToManyField(Superinvestor, blank=True)

    class Meta:
        verbose_name = "Lista de superinvestor favoritas"
        verbose_name_plural = "Lista de superinvestor favoritas"
        db_table = "favorites_superinvestor_list"

    def __str__(self):
        return self.user.username


class Period(Model):
    PERIODS = ((1, '1 Quarter'), (2, '2 Quarter'), (3, '3 Quarter'), (4, '4 Quarter'))
    year = DateField(null=True, blank=True)
    period = IntegerField(choices=PERIODS, null=True, blank=True)

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        db_table = "assets_periods"
        ordering = ['period', 'year']
        get_latest_by = ['period', 'year']
    
    def __str__(self):
        return f'{self.period}-{str(self.year)}'


class BaseSuperinvestorHoldingsInformation(Model):
    period_related = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    company_name = TextField(blank=True, null=True)
    not_registered_company = BooleanField(default=False)
    need_verify_company = BooleanField(default=False)
    portfolio_change = FloatField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    @property
    def actual_company(self):
        return self.company if self.company else self.company_name
    
    @property
    def actual_company_image(self):
        image = None
        if type(self.actual_company) != str:
            image = self.actual_company.image
        return image
    
    @property
    def actual_company_ticker(self):
        ticker = None
        if type(self.actual_company) != str:
            ticker = self.actual_company.ticker
        return ticker


class SuperinvestorActivity(BaseSuperinvestorHoldingsInformation):
    MOVE = ((1, 'Compra'), (2, 'Venta'))

    superinvestor_related = ForeignKey(
        Superinvestor, on_delete=SET_NULL, 
        null=True, blank=True, related_name='positions'
    )
    percentage_share_change = FloatField(null=True, blank=True)
    share_change = FloatField(null=True, blank=True)
    is_new = BooleanField(default=False)
    movement = PositiveIntegerField(choices=MOVE, null=True, blank=True)

    class Meta:
        verbose_name = "Superinvestor activity"
        verbose_name_plural = "Superinvestors activity"
        db_table = "superinvestors_activity"

    def __str__(self):
        return f'{self.superinvestor_related.name}-{self.period_related}-{self.actual_company}'
    

class SuperinvestorHistory(BaseSuperinvestorHoldingsInformation):
    superinvestor_related = ForeignKey(
        Superinvestor, on_delete=SET_NULL, 
        null=True, blank=True, related_name='history'
    )
    movement = CharField(max_length=500, null=True, blank=True)
    shares = FloatField(null=True, blank=True)
    reported_price = FloatField(null=True, blank=True)
    portfolio_weight = FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Superinvestor history"
        verbose_name_plural = "Superinvestors history"
        db_table = "superinvestors_history"
    
    @property
    def total_value(self):
        return self.shares * self.reported_price