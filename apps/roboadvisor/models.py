from django.db.models import (
    Model,
    SET_NULL,
    CASCADE,
    ForeignKey,
    DateTimeField,
    BooleanField,
    IntegerField,
    ManyToManyField,
    DecimalField,
    OneToOneField,
    CharField,
    TextField,
    PositiveBigIntegerField,
    PositiveIntegerField
)
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

from apps.general.models import Tag, Category
from apps.empresas.models import Company

from .constants import *

User = get_user_model()


class BaseInvestorProfile(Model):
    created_at = DateTimeField(auto_now_add=True)
    horizon = IntegerField(null=True, blank=True, choices=HORIZON)
    risk_profile = IntegerField(null=True, blank=True, choices=RISK_PROFILE)
    investor_type = IntegerField(null=True, blank=True, choices=INVESTOR_TYPE)

    class Meta:
        abstract = True


class InvestorProfile(BaseInvestorProfile):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name='user_investor_profile')
    updated_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User investor profile"
        db_table = "user_investor_profile"
    
    def __str__(self) -> str:
        return self.user.username


class TemporaryInvestorProfile(BaseInvestorProfile):
    profile_related = ForeignKey(InvestorProfile, on_delete=SET_NULL, null=True, related_name='temporary_investor')

    class Meta:
        verbose_name = "Temporary investor profile"
        db_table = "temporary_investor_profile"
    
    def __str__(self) -> str:
        return self.profile_related.user.username


class RoboAdvisorService(Model):
    price = PositiveBigIntegerField(null=True, blank=True)
    order = PositiveIntegerField(null=True, blank=True)
    available = BooleanField(default=True)
    title = CharField(max_length=500, null=True, blank=True)
    description = TextField(null=True, blank=True)
    slug = CharField(max_length=500, null=True, blank=True)
    category = ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True)
    tags = ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Roboadvisor services"
        db_table = "roboadvisor_services"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save()
    
    def get_absolute_url(self):
        return reverse("roboadvisor:robo-option", kwargs={"slug": self.slug})


class BaseRoboAdvisorQuestion(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True) 
    service = ForeignKey(RoboAdvisorService, on_delete=SET_NULL, null=True)
    date_started = DateTimeField(auto_now_add=True)
    date_finished = DateTimeField(null=True, blank=True)
    status = IntegerField(null=True, blank=True, choices=SERVICE_STATUS)
    slug = CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True
    
    def save(self) -> None:
        if not self.slug:
            self.slug = slugify(self.user.id)
        return super().save()


class RoboAdvisorQuestionFinancialSituation(BaseRoboAdvisorQuestion):
    average_income = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    average_expense = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    debt = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    recurrent_savings = BooleanField(default = False)
    recurrent_debts = BooleanField(default = False)
    savings = DecimalField (default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    debt_percentage = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    saving_percentage = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    number_sources_income = IntegerField(default = 1, blank=True) 
    
    class Meta:
        verbose_name = 'RoboAdvisor Financial Situation'
        verbose_name_plural = 'RoboAdvisor Financial Situations'
        db_table = "roboadvisor_financial_situation"

    def __str__(self):
        pass


class BaseRoboAdvisorQuestionAsset(Model):
    PERIODS = (
        (1, 'Horas'),
        (2, 'Días'),
        (3, 'Semanas'),
        (4, 'Meses'),
        (5, 'Años')
    )
    HOURS = ((x, f'{x}') for x in range(0,25))
    DAYS = ((x, f'{x}') for x in range(0,8))

    asset = None
    result = None
    sector_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE)
    asset_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE)
    amount_time_studied = PositiveIntegerField(default = 0)
    period_time_studied = PositiveIntegerField(default = 4, choices=PERIODS)
    number_shares = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    capital_invested = DecimalField(default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    sector_relationship = TextField(default = '')
    time_studing = IntegerField(null=True, blank=True, choices=HOURS)
    days_studing = IntegerField(null=True, blank=True, choices=DAYS)  

    class Meta:
        abstract = True


class RoboAdvisorQuestionInvestorExperience(BaseRoboAdvisorQuestion, BaseRoboAdvisorQuestionAsset):
    age = PositiveIntegerField(null=True, blank=True)
    objectif = IntegerField(choices=OBJECTIFS, null=True, blank=True) 
    investor_type_self_definition = IntegerField(null=True, blank=True,choices=INVESTOR_TYPE)
    percentage_invested = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    already_investing = BooleanField(default=False)
    percentage_anualized_revenue = DecimalField (null=True, blank=True, default=0, max_digits=10, decimal_places=2)
    years_investing = PositiveIntegerField(null=True,default=0, blank=True)    

    class Meta:
        verbose_name = "Pregunta: Historial del inversor"
        verbose_name_plural = "Pregunta: Historial del inversor"
        db_table = "roboadvisor_investor experience"


class RoboAdvisorQuestionRiskAversion(BaseRoboAdvisorQuestion):       
    volatilidad = IntegerField(choices=VOLATILIDAD,null=True, blank=True)
    percentage_for_onefive = IntegerField (null=True, blank=True)
    percentage_for_three = IntegerField (null=True, blank=True)
    percentage_for_fourfive = IntegerField (null=True, blank=True)
    percentage_for_zerofive = IntegerField (null=True, blank=True)
    percentage_in_one_stock = IntegerField (null=True, blank=True)
    number_stocks = IntegerField(null=True, blank=True, choices=NUMBER_STOCKS)
    
    class Meta:
        verbose_name = "Pregunta: Aversión al riesgo"
        verbose_name_plural = "Pregunta: Aversión al riesgo"
        db_table = "roboadvisor_risk_aversion"
        

class RoboAdvisorQuestionHorizon(BaseRoboAdvisorQuestion):    
    horizon_years = PositiveIntegerField(null=True, blank=True)
    comment = TextField(default = '')
    
    class Meta:
        verbose_name = "Pregunta: Horizote de inversión"
        verbose_name_plural = "Pregunta: Horizote de inversión"
        db_table = "roboadvisor_horizon"
        

class RoboAdvisorQuestionPortfolioAssetsWeight(BaseRoboAdvisorQuestion):
    etfs_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    stocks_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    bonds_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    real_estate_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    sofipos_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2,  validators=[MinValueValidator(0), MaxValueValidator(100)])
    cryptos_percentage = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = "Pregunta: Gusto por activos"
        verbose_name_plural = "Pregunta: Gusto por activos"
        db_table = "roboadvisor_assets_weight"


class RoboAdvisorQuestionCompanyAnalysis(BaseRoboAdvisorQuestion, BaseRoboAdvisorQuestionAsset):
    asset = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    result = IntegerField(null=True, blank=True, choices=RESULTS)

    class Meta:
        verbose_name = "Pregunta: Decisión compañía"
        verbose_name_plural = "Pregunta: Decisión compañía"
        db_table = "roboadvisor_company_analysis"


class RoboAdvisorQuestionPortfolioComposition(BaseRoboAdvisorQuestionAsset):
    asset = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Pregunta: Composición portfolio empresas"
        verbose_name_plural = "Pregunta: Composición portfolio empresas"
        db_table = "roboadvisor_stocks_portfolio_positions"

    def __str__(self):
        return str(f'{self.investor_related.user.username} - {self.id}')


class RoboAdvisorQuestionStocksPortfolio(BaseRoboAdvisorQuestion):
    stocks = ManyToManyField(RoboAdvisorQuestionPortfolioComposition)
    
    class Meta:
        verbose_name = "Pregunta: Portfolio"
        verbose_name_plural = "Pregunta: Portfolio"
        db_table = "roboadvisor_stocks_portfolio"
