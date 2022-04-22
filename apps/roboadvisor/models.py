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

from apps.general.models import Tag, Category, Currency
from apps.empresas.models import Company

from .constants import *

User = get_user_model()

# Create a quiz arround sectors and companies to see if the user knows the company and the sector enought to invest in

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
        verbose_name_plural = 'Users investor profiles'
        db_table = "user_investor_profile"
    
    def __str__(self) -> str:
        return self.user.username


class TemporaryInvestorProfile(BaseInvestorProfile):
    profile_related = ForeignKey(InvestorProfile, on_delete=SET_NULL, null=True, related_name='temporary_investor')

    class Meta:
        verbose_name = "Temporary investor profile"
        verbose_name_plural = 'Temporary investor profiles'
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
    thumbnail = CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Roboadvisor service"
        verbose_name_plural = 'Roboadvisor services'
        db_table = "roboadvisor_services"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save()
    
    def get_absolute_url(self):
        return reverse("roboadvisor:robo-option", kwargs={"slug": self.slug})


class RoboAdvisorServiceStep(Model):
    title = CharField(max_length=500, null=True, blank=True)
    description = TextField(null=True, blank=True)    
    order = PositiveIntegerField(null=True, blank=True)
    url = CharField(max_length=500, null=True, blank=True)
    template = CharField(max_length=500, null=True, blank=True)
    service_related = ForeignKey(RoboAdvisorService, on_delete=SET_NULL, null=True, blank=True, related_name="steps")

    class Meta:
        ordering = ['order']
        verbose_name = "Roboadvisor service step"
        verbose_name_plural = 'Roboadvisor service steps'
        db_table = "roboadvisor_service_steps"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self) -> None:
        if not self.template:
            self.template = slugify(self.title)
        return super().save()
    
    @property
    def template_path(self):
        return f'roboadvisor/steps/{self.template}.html'
    
    @property
    def url_path(self):
        return f'roboadvisor:{self.url}'


class RoboAdvisorUserServiceActivity(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    service = ForeignKey(RoboAdvisorService, on_delete=SET_NULL, null=True)
    date_started = DateTimeField(auto_now_add=True)
    date_finished = DateTimeField(null=True, blank=True)
    status = IntegerField(choices=SERVICE_STATUS, default=SERVICE_STATUS[2][0])

    class Meta:
        verbose_name = 'RoboAdvisor Service Activity'
        verbose_name_plural = 'RoboAdvisor Service Activity'
        db_table = "roboadvisor_service_activity"
    
    def __str__(self) -> str:
        return self.service.title


class RoboAdvisorUserServiceStepActivity(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    step = ForeignKey(RoboAdvisorServiceStep, on_delete=SET_NULL, null=True)
    date_started = DateTimeField(null=True, blank=True)
    date_finished = DateTimeField(auto_now_add=True)
    status = IntegerField(choices=SERVICE_STATUS, default=SERVICE_STATUS[2][0])

    class Meta:
        verbose_name = 'RoboAdvisor Service Step Activity'
        verbose_name_plural = 'RoboAdvisor Service Steps Activity'
        db_table = "roboadvisor_service_step_activity"
    
    def __str__(self) -> str:
        return self.step.title


class BaseRoboAdvisorQuestion(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    service_activity = ForeignKey(RoboAdvisorUserServiceActivity, on_delete=SET_NULL, null=True)
    service_step = ForeignKey(RoboAdvisorUserServiceStepActivity, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        return f'{self.user.username} - {self.service_activity.service.title} - {self.service_step.step.title}'


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
    currency = ForeignKey(Currency, null=True, blank=True, on_delete=SET_NULL)
    
    class Meta:
        verbose_name = 'RoboAdvisor Financial Situation'
        verbose_name_plural = 'RoboAdvisor Financial Situations'
        db_table = "roboadvisor_financial_situation"


class BaseRoboAdvisorHorizon(BaseRoboAdvisorQuestion):
    horizon_time = PositiveIntegerField(default = 0)
    horizon_period = PositiveIntegerField(default = 4, choices=PERIODS)
    comment = TextField(default = '')

    class Meta:
        abstract = True


class BaseRoboAdvisorQuestionAsset(BaseRoboAdvisorHorizon):
    asset = None
    result = None
    sector_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE, default=4)
    asset_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE, default=4)
    amount_time_studied = PositiveIntegerField(default = 0)
    period_time_studied = PositiveIntegerField(default = 4, choices=PERIODS)
    number_shares = DecimalField(null=True, default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    capital_invested = DecimalField(null=True, default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    sector_relationship = TextField(default = '')

    class Meta:
        abstract = True


class RoboAdvisorQuestionInvestorExperience(BaseRoboAdvisorQuestion):
    age = PositiveIntegerField(null=True, blank=True, default=18)
    objectif = IntegerField(choices=OBJECTIFS, null=True, blank=True, default=1) 
    investor_type_self_definition = IntegerField(null=True, blank=True, choices=INVESTOR_TYPE, default=1)
    percentage_invested = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_anualized_revenue = DecimalField (null=True, blank=True, default=0, max_digits=10, decimal_places=2)
    time_investing_exp = PositiveIntegerField(default = 0)
    period_investing_exp = PositiveIntegerField(default = 4, choices=PERIODS)  

    class Meta:
        verbose_name = "Pregunta: Experiencia como inversor"
        verbose_name_plural = "Pregunta: Experiencia como inversor"
        db_table = "roboadvisor_investor_experience"


class RoboAdvisorQuestionRiskAversion(BaseRoboAdvisorHorizon):       
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


class RoboAdvisorQuestionCompanyAnalysis(BaseRoboAdvisorQuestionAsset):
    asset = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
    result = IntegerField(null=True, blank=True, choices=RESULTS)
    number_shares = None
    capital_invested = None

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


class RoboAdvisorQuestionStocksPortfolio(BaseRoboAdvisorQuestion):
    stocks = ManyToManyField(RoboAdvisorQuestionPortfolioComposition)
    
    class Meta:
        verbose_name = "Pregunta: Portfolio"
        verbose_name_plural = "Pregunta: Portfolio"
        db_table = "roboadvisor_stocks_portfolio"
