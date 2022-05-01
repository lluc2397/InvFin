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

from .constants import (
    HORIZON,
    RISK_PROFILE,
    INVESTOR_TYPE,
    ROBO_RESULTS,
    ROBO_STEPS,
    PERIODS,
    KNOWLEDGE,
    OBJECTIFS,
    NUMBER_STOCKS,
    SERVICE_STATUS,
    VOLATILIDAD,
    RESULTS,
    PROFILE_VERY_AGRESIVE,
    PROFILE_AGRESIVE,
    PROFILE_CONSERVATIVE,
    PROFILE_REGULAR,
    PROFILE_VERY_CONSERVATIVE
)

User = get_user_model()

# Create a quiz arround sectors and companies to see if the user knows the company and the sector enought to invest in

class BaseInvestorProfile(Model):
    created_at = DateTimeField(auto_now_add=True)
    horizon = CharField(max_length=500, null=True, blank=True, choices=HORIZON)
    risk_profile = CharField(max_length=500, blank=True, choices=RISK_PROFILE)
    investor_type = CharField(max_length=500, null=True, blank=True, choices=INVESTOR_TYPE)

    class Meta:
        abstract = True
    
    @property
    def explanation(self):
        if self.risk_profile == 'very-agressive':
            return PROFILE_VERY_AGRESIVE
        elif self.risk_profile == 'agressive':
            return PROFILE_AGRESIVE
        elif self.risk_profile == 'regular':
            return PROFILE_REGULAR
        elif self.risk_profile == 'conservative':
            return PROFILE_CONSERVATIVE
        return PROFILE_VERY_CONSERVATIVE


class InvestorProfile(BaseInvestorProfile):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, related_name='user_investor_profile')
    updated_at = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User investor profile"
        verbose_name_plural = 'Users investor profiles'
        db_table = "user_investor_profile"
    
    def __str__(self) -> str:
        return self.user.username


class RoboAdvisorService(Model):
    price = PositiveBigIntegerField(null=True, blank=True)
    order = PositiveIntegerField(null=True, blank=True)
    available = BooleanField(default=True)
    title = CharField(max_length=500, null=True, blank=True)
    description = TextField(null=True, blank=True)
    slug = CharField(max_length=500, null=True, blank=True, choices=ROBO_RESULTS)
    category = ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True)
    tags = ManyToManyField(Tag, blank=True)
    thumbnail = CharField(max_length=500, null=True, blank=True)
    template_result = CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Roboadvisor service"
        verbose_name_plural = 'Roboadvisor services'
        db_table = "roboadvisor_services"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self) -> None:
        self.template_result = self.slug            
        return super().save()
    
    def get_absolute_url(self):
        return reverse("roboadvisor:robo-option", kwargs={"slug": self.slug})
    
    @property
    def template_path(self):
        return f'roboadvisor/results/{self.template_result}.html'


class RoboAdvisorServiceStep(Model):
    title = CharField(max_length=500, null=True, blank=True)
    slug = CharField(max_length=500, null=True, blank=True)
    description = TextField(null=True, blank=True)    
    order = PositiveIntegerField(null=True, blank=True)
    url = CharField(max_length=500, null=True, blank=True, choices=ROBO_STEPS)
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
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.service_related.title}')
        if not self.template:
            self.template = self.url
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
    status = CharField(max_length=500, choices=SERVICE_STATUS, default='started')

    class Meta:
        verbose_name = 'RoboAdvisor Service Activity'
        verbose_name_plural = 'RoboAdvisor Service Activity'
        db_table = "roboadvisor_service_activity"
    
    def __str__(self) -> str:
        return f'{self.service.title} - {self.id}' 
    
    @property
    def company_related(self):
        if self.service.slug == 'company-match' and RoboAdvisorQuestionCompanyAnalysis.objects.filter(service_activity = self).exists():
            return True
        return False
    
    @property
    def temp_profile_related(self):
        if self.service.slug == 'investor-profile' and TemporaryInvestorProfile.objects.filter(service_activity = self).exists():
            return True
        return False
    
    @property
    def service_result(self):
        if self.company_related:
            service_question = self.roboadvisorquestioncompanyanalysis
            asset = service_question.asset
            title = f'{asset.name} ({asset.ticker}) parece estar en un momento para'
            result = service_question.result
            explanation = asset.short_introduction
            extra = asset
        if self.temp_profile_related:
            service_question = self.temporaryinvestorprofile
            title = f'Parece que tienes un perfil de inversor'
            result = service_question.risk_profile
            explanation = service_question.explanation

        return {
            'title': title,
            'result': result,
            'explanation': explanation,
            'extra':extra
        }

    @property
    def metadata(self):
        thumbnail = self.service.thumbnail
        title = self.service.title
        if self.company_related:
            thumbnail = self.roboadvisorquestioncompanyanalysis.asset.image
            title = f'{title} - {self.roboadvisorquestioncompanyanalysis.asset.ticker}'
        metadata = {
            'title':title,
            'thumbnail':thumbnail
        }
        return metadata


class TemporaryInvestorProfile(BaseInvestorProfile):
    profile_related = ForeignKey(InvestorProfile, on_delete=SET_NULL, null=True, related_name='temporary_investor')
    service_activity = OneToOneField(RoboAdvisorUserServiceActivity, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Temporary investor profile"
        verbose_name_plural = 'Temporary investor profiles'
        db_table = "temporary_investor_profile"
    
    def __str__(self) -> str:
        return self.profile_related.user.username



class RoboAdvisorUserServiceStepActivity(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    step = ForeignKey(RoboAdvisorServiceStep, on_delete=SET_NULL, null=True)
    date_started = DateTimeField(null=True, blank=True)
    date_finished = DateTimeField(auto_now_add=True)
    status = CharField(max_length=500, choices=SERVICE_STATUS, default='started')

    class Meta:
        verbose_name = 'RoboAdvisor Service Step Activity'
        verbose_name_plural = 'RoboAdvisor Service Steps Activity'
        db_table = "roboadvisor_service_step_activity"
    
    def __str__(self) -> str:
        return self.step.title


class BaseRoboAdvisorQuestion(Model):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    service_activity = OneToOneField(RoboAdvisorUserServiceActivity, on_delete=SET_NULL, null=True)
    service_step = OneToOneField(RoboAdvisorUserServiceStepActivity, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        # return f'{self.user.username} - {self.service_activity.service.title} - {self.service_step.step.title}'
        return f'{self.id}'


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
    horizon_period = CharField(max_length=500, default=PERIODS[4], choices=PERIODS)
    comment = TextField(default = '')

    class Meta:
        abstract = True


class BaseRoboAdvisorQuestionAsset(BaseRoboAdvisorHorizon):
    asset = None
    result = None
    sector_knowledge = CharField(max_length=500, null=True, blank=True, choices=KNOWLEDGE, default=KNOWLEDGE[4])
    asset_knowledge = CharField(max_length=500, null=True, blank=True, choices=KNOWLEDGE, default=KNOWLEDGE[4])
    amount_time_studied = PositiveIntegerField(default = 0)
    period_time_studied = CharField(max_length=500, default=PERIODS[4], choices=PERIODS)
    number_shares = DecimalField(null=True, default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    capital_invested = DecimalField(null=True, default = 0, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    sector_relationship = TextField(default = '')

    class Meta:
        abstract = True


class RoboAdvisorQuestionInvestorExperience(BaseRoboAdvisorQuestion):
    age = PositiveIntegerField(null=True, blank=True, default=18)
    objectif = IntegerField(choices=OBJECTIFS, null=True, blank=True, default=1) 
    investor_type_self_definition = CharField(max_length=500, null=True, blank=True, choices=INVESTOR_TYPE, default=INVESTOR_TYPE[1])
    percentage_invested = DecimalField(blank=True, default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    percentage_anualized_revenue = DecimalField (null=True, blank=True, default=0, max_digits=10, decimal_places=2)
    time_investing_exp = PositiveIntegerField(default = 0)
    period_investing_exp = CharField(max_length=500, default=PERIODS[4], choices=PERIODS)  

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
