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

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

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
    title = CharField(max_length=500, null=True, blank=True)
    description = TextField(null=True, blank=True)
    price = PositiveBigIntegerField(null=True, blank=True)
    order = PositiveIntegerField(null=True, blank=True)
    slug = CharField(max_length=500, null=True, blank=True)
    available = BooleanField(default=True)
    times_asked = PositiveBigIntegerField(default=0)
    times_used = PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['-order']
        verbose_name = "Roboadvisor services"
        db_table = "roboadvisor_services"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save()


# class BaseRoboAdvisorService(Model):
#     user = ForeignKey(User, on_delete=SET_NULL, null=True) 
#     service = ForeignKey(RoboAdvisorService, on_delete=SET_NULL, null=True) 
#     date_started = DateTimeField(auto_now_add=True)
#     date_finished = DateTimeField(null=True, blank=True)
#     status = IntegerField(null=True, blank=True, choices=SERVICE_STATUS)
#     title = CharField(max_length=500, null=True, blank=True)
#     description = TextField(null=True, blank=True)
#     slug = CharField(max_length=500, null=True, blank=True)

#     class Meta:
#         abstract = True


# class RoboAdvisorServiceUsed(BaseRoboAdvisorService):
#     title = None
#     description = None
#     slug = None

#     class Meta:
#         verbose_name = "Roboadvisor services used"
#         db_table = "roboadvisor_services_used"
    
#     def __str__(self) -> str:
#         return f'{self.user.username} - {self.service.title}'


# class RoboAdvisorQuestionFinancialSituation(BaseRoboAdvisorService):
#     income = DecimalField (null=True, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)] )
#     expense = DecimalField (null=True, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
#     debt = DecimalField (null=True, blank=True, max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])

#     class Meta:
#         verbose_name = 'RoboAdvisor Financial Situation'
#         verbose_name_plural = 'RoboAdvisor Financial Situations'
#         db_table = "roboadvisor_financial_situation"

#     def __str__(self):
#         pass


# class RoboAdvisorQuestionInvestorExperience(BaseRoboAdvisorService):      
#     age = PositiveIntegerField(null=True, blank=True)
#     objectif = IntegerField(choices=OBJECTIFS, null=True, blank=True) 
#     investor_type_self_definition = IntegerField(null=True, blank=True,choices=INVESTOR_TYPE)
#     percentage_invested = DecimalField (null=True, blank=True, default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     already_investing = BooleanField(default=False)
#     percentage_anualized_revenue = DecimalField (null=True, blank=True, default=0, max_digits=10, decimal_places=2)
#     years_investing = PositiveIntegerField(null=True,default=0, blank=True)   

#     class Meta:
#         verbose_name = "Pregunta: Historial del inversor"
#         verbose_name_plural = "Pregunta: Historial del inversor"
#         db_table = "roboadvisor_investor experience"


# class RoboAdvisorQuestionStudyTime(BaseRoboAdvisorService):
#     HOURS = ((x, f'{x}') for x in range(0,25))
#     DAYS = ((x, f'{x}') for x in range(0,8))
#     time_studing = IntegerField(null=True, blank=True, choices=HOURS)
#     days_studing = IntegerField(null=True, blank=True, choices=DAYS)    

#     class Meta:
#         verbose_name = "Pregunta: Tiempo de estudio"
#         verbose_name_plural = "Pregunta: Tiempo de estudio"
#         db_table = "roboadvisor_study_time"
        

# class RoboAdvisorQuestionRiskAversion(BaseRoboAdvisorService):       
#     volatilidad = IntegerField(choices=VOLATILIDAD,null=True, blank=True)
#     percentage_for_onefive = IntegerField (null=True, blank=True)
#     percentage_for_three = IntegerField (null=True, blank=True)
#     percentage_for_fourfive = IntegerField (null=True, blank=True)
#     percentage_for_zerofive = IntegerField (null=True, blank=True)
#     percentage_in_one_stock = IntegerField (null=True, blank=True)
#     number_stocks = IntegerField(null=True, blank=True, choices=NUMBER_STOCKS)
    
#     class Meta:
#         verbose_name = "Pregunta: Aversión al riesgo"
#         verbose_name_plural = "Pregunta: Aversión al riesgo"
#         db_table = "roboadvisor_risk_aversion"
        

# class RoboAdvisorQuestionHorizon(BaseRoboAdvisorService):    
#     horizon_years = PositiveIntegerField(null=True, blank=True)
#     comment = TextField(null=True, blank=True)
    
#     class Meta:
#         verbose_name = "Pregunta: Horizote de inversión"
#         verbose_name_plural = "Pregunta: Horizote de inversión"
#         db_table = "roboadvisor_horizon"
        

# class RoboAdvisorQuestionPortfolioAssetsWeight(BaseRoboAdvisorService):
#     etfs = BooleanField(default=False)
#     etfs_percentage =DecimalField(null=True, default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     stocks = BooleanField(default=False)
#     stocks_percentage =DecimalField(null=True,default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     bonds = BooleanField(default=False)
#     bonds_percentage =DecimalField(null=True,default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     real_estate = BooleanField(default=False)
#     real_estate_percentage =DecimalField(null=True,default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     sofipos = BooleanField(default=False)
#     sofipos_percentage =DecimalField(null=True,default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     cryptos = BooleanField(default=False)
#     cryptos_percentage =DecimalField(null=True, blank=True,default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
#     class Meta:
#         verbose_name = "Pregunta: Gusto por activos"
#         verbose_name_plural = "Pregunta: Gusto por activos"
#         db_table = "roboadvisor_assets_weight"


# class RoboAdvisorQuestionCompanyAnalysis(BaseRoboAdvisorService):
#     company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
#     result = IntegerField(null=True, blank=True, choices=RESULTS)
#     sector_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE)

#     class Meta:
#         verbose_name = "Pregunta: Decisión compañía"
#         verbose_name_plural = "Pregunta: Decisión compañía"
#         db_table = "roboadvisor_company_analysis"


# class RoboAdvisorQuestionStocksPortfolio(BaseRoboAdvisorService):
    
#     class Meta:
#         verbose_name = "Pregunta: Portfolio"
#         verbose_name_plural = "Pregunta: Portfolio"
#         db_table = "roboadvisor_stocks_portfolio"


# class RoboAdvisorQuestionPortfolioComposition(Model):
#     company = ForeignKey(Company, on_delete=SET_NULL, null=True, blank=True)
#     number_shares = DecimalField(null=True, blank=True)
#     capital_invested = DecimalField(null=True, blank=True)    
#     sector_knowledge = IntegerField(null=True, blank=True, choices=KNOWLEDGE)
#     portfolio_related = ForeignKey(RoboAdvisorQuestionStocksPortfolio, on_delete=SET_NULL,null=True, blank=True)

#     class Meta:
#         verbose_name = "Pregunta: Composición portfolio empresas"
#         verbose_name_plural = "Pregunta: Composición portfolio empresas"
#         db_table = "roboadvisor_stocks_portfolio_positions"

#     def __str__(self):
#         return str(f'{self.investor_related.user.username} - {self.id}')


# # class QUESTIONS_PORTFOLIO_ETF_COMPOSITIONS(Model):
# #     etf_related = ForeignKey(ETF, on_delete=SET_NULL,null=True, blank=True)
# #     number_shares = FloatField(null=True, blank=True)
# #     capital_invested = FloatField(null=True, blank=True)
    
# #     portfolio_related = ForeignKey(QUESTIONS_PORTFOLIO,on_delete=SET_NULL,null=True, blank=True)
# #     currency = IntegerField(null=True, blank=True, choices=CURRENCY)

# #     class Meta:
# #         verbose_name = "Pregunta: Composición portfolio ETF"
# #         verbose_name_plural = "Pregunta: Composición portfolio ETF"

# #     def __str__(self):
# #         return str(f'{self.investor_related.user.username} - {self.id}')