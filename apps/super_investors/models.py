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
    def portfolio_information(self):
        all_history = self.history.prefetch_related(
            'period_related', 'company'
            ).all()
        all_companies = self.history.order_by().values(
            'company', 'company_name'
            ).distinct('company', 'company_name')
        portfolio = []
        for company in all_companies:
            query_company_history = self.history.filter(**company)
            
            if query_company_history.last().shares != 0:
                portfolio.append(query_company_history.last())
        
        total_number_of_holdings = len(portfolio)
        portfolio_value = sum(position.total_value for position in portfolio)
        top_holdings = sorted(portfolio, key=lambda x : x.portfolio_weight)
        sectors_invested = set()
        for company in portfolio:
            sectors_invested.add(company.company_sector)
                
            
        num_sectors = len(sectors_invested)
        return {
            'portfolio': portfolio, 
            'all_history': all_history,
            'total_number_of_holdings': total_number_of_holdings,
            'portfolio_value': portfolio_value,
            'top_holdings': top_holdings[:5],
            'sectors_invested': sectors_invested,
            'num_sectors': num_sectors
        }
    
    @property
    def all_information(self):
        portfolio_information = self.portfolio_information
        portfolio_information['all_activity'] = self.positions.all()
        return portfolio_information


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
        ordering = ['-year', '-period']
        get_latest_by = ['-year', '-period']
    
    def __str__(self):
        return f'Q{self.period} {str(self.year.year)}'


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
        actual_company = {}
        if self.company:
            actual_company['company'] = self.company
        else: 
            actual_company['company_name'] = self.company_name
        return actual_company
    
    @property
    def actual_company_info(self):
        actual_company_info = {}
        if self.company:
            company = self.company
            actual_company_info['full_name'] = f'({company.ticker}) {company.name}'
            actual_company_info['image'] = company.image
            actual_company_info['ticker'] = company.ticker
        else:
            actual_company_info['full_name'] = self.company_name
            actual_company_info['image'] = None
            actual_company_info['ticker'] = None
        return actual_company_info
    
    @property
    def company_sector(self):
        sector = None
        if self.company:
            sector = self.company.sector
        return sector


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
        ordering = ['period_related']
        get_latest_by = ['period_related']

    def __str__(self):
        return f'{self.superinvestor_related.name}-{self.period_related}-{self.actual_company}'
    
    @property
    def movement_type(self):
        movement_type = {'move': 'Venta', 'color': 'danger'}
        if self.movement == 1:
            movement_type = {'move': 'Compra', 'color': 'success'}
        return movement_type
    

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
        ordering = ['period_related']
        get_latest_by = ['period_related']
    
    def __str__(self):
        return f'{self.superinvestor_related.name}-{self.period_related}-{self.actual_company}'
    
    @property
    def total_value(self):
        return self.shares * self.reported_price
    
    @property
    def movement_type(self):
        movement_type = {'move': 'Venta', 'color': 'danger'}
        if self.movement.startswith('Add') or self.movement.startswith('Buy'):
            movement_type = {'move': 'Compra', 'color': 'success'}
        return movement_type