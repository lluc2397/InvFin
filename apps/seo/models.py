from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    ManyToManyField,
    PositiveBigIntegerField,
    JSONField,
    SlugField
)
from django.utils import timezone
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.constants import SOCIAL_MEDIAS
from . import constants 

User = get_user_model()


class Visiteur(Model):
    ip = CharField(max_length=50, null=True, blank=True)
    session_id = CharField(max_length=10000, null=True, blank=True)
    HTTP_USER_AGENT = CharField(max_length=10000, null=True, blank=True)
    country_code = CharField(max_length=10000, null=True, blank=True)
    country_name = CharField(max_length=10000, null=True, blank=True)
    dma_code = CharField(max_length=10000, null=True, blank=True)
    is_in_european_union = BooleanField(null=True, blank=True)
    latitude = CharField(max_length=10000, null=True, blank=True)
    longitude = CharField(max_length=10000, null=True, blank=True)
    city = CharField(max_length=10000, null=True, blank=True)
    region = CharField(max_length=10000, null=True, blank=True)
    time_zone = CharField(max_length=10000, null=True, blank=True)
    postal_code = CharField(max_length=10000, null=True, blank=True)
    continent_code = CharField(max_length=10000, null=True, blank=True)
    continent_name = CharField(max_length=10000, null=True, blank=True)
    first_visit_date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visiteur"
        db_table = "visiteurs"
    
    def __str__(self):
        return str(self.id)
    

class MetaParameters(Model):
    meta_title = CharField(max_length=999,null=True, blank=True)
    meta_description = TextField(null=True, blank=True)
    meta_img = CharField(max_length=999,null=True, blank=True)
    meta_url = CharField(max_length=999,null=True, blank=True)
    meta_keywords = TextField()
    meta_author = ForeignKey(User, on_delete=SET_NULL, null=True)
    published_time = DateTimeField(auto_now=True)
    modified_time = DateTimeField(auto_now=True)
    created_at = DateTimeField(default=timezone.now)    
    views = PositiveBigIntegerField(default=0)
    schema_org = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Meta information"
        db_table = "meta_information"

    def __str__(self):
        return self.meta_title


class MetaParametersHistorial(Model):
    parameter_settings = ForeignKey(MetaParameters, on_delete= CASCADE, null=True)
    in_use = BooleanField(default=True)

    class Meta:
        verbose_name = "Historial meta información"
        db_table = "meta_information_historial"

    def __str__(self):
        return self.parameter_settings.meta_title


class Journey(Model):
    date = DateTimeField(auto_now_add=True)
    current_path = CharField(max_length=2000, null=True, blank=True)
    comes_from = CharField(max_length=2000, null=True, blank=True)

    class Meta:
        abstract = True


class VisiteurJourney(Journey):
    user = ForeignKey(Visiteur, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas anónimos"
        db_table = "visits_historial_visiteurs"
    

class UsersJourney(Journey):
    user = ForeignKey(User, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas usuarios"
        db_table = "visits_historial_users"


class PromotionCampaign(Model):
    title = CharField(max_length=600, blank=True)
    slug = SlugField(blank=True)
    categories = ManyToManyField('general.Category', blank=True)
    tags = ManyToManyField('general.Tag', blank=True)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Promotions campaigns"
        db_table = "promotions_campaigns"

    def __str__(self) -> str:
        return self.title


class Promotion(Model):
    MEDIUMS = [
        ('ads', 'Ads'), 
        ('email', 'Email'), 
        ('invfin', 'Web'), 
        ('social-media-posts', 'Social media posts')]

    title = CharField(max_length=600, blank=True)
    content = RichTextField()
    thumbnail = CharField(max_length=600, blank=True)
    slug = SlugField()
    prize = PositiveBigIntegerField(default=0)
    has_prize = BooleanField(default=False)
    shareable_url = CharField(max_length=600, blank=True)
    redirect_to = CharField(max_length=600, blank=True)
    medium = CharField(max_length=250, choices=MEDIUMS, blank=True)
    web_promotion_type = CharField(max_length=250, choices=constants.WEP_PROMOTION_TYPE, blank=True)
    web_location = CharField(max_length=250, choices=constants.WEP_PROMOTION_LOCATION, blank=True)
    social_media = CharField(max_length=250, blank=True, choices=SOCIAL_MEDIAS)
    publication_date = DateTimeField(blank=True)
    campaign_related = ForeignKey(PromotionCampaign, on_delete=SET_NULL, null=True, blank=True)
    reuse = BooleanField(default=False)
    times_to_reuse = PositiveBigIntegerField(default=0)
    users_clicked = ManyToManyField(User, blank=True)
    visiteurs_clicked = ManyToManyField(Visiteur, blank=True)
    clicks_by_user = PositiveBigIntegerField(default=0)
    clicks_by_not_user = PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = "Promociones"
        db_table = "promotions"
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def full_url(self):
        source = 'invfin'
        if self.medium != source:            
            source = self.social_media
        utm_source = f'utm_source={source}'
        utm_medium = f'utm_medium={self.medium}'
        utm_campaign = f'utm_campaign={self.campaign_related.title}'
        utm_term = f'utm_term={self.title}'
        return f'{self.redirect_to}?{utm_source}&{utm_medium}&{utm_campaign}&{utm_term}'


class BaseModelVisited(Model):
    date = DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        try:
            response = self.user.username
        except:
            response = f'Visiteur - {self.user.id}'
        return response


class BaseVisiteurModelVisited(BaseModelVisited):
    user = ForeignKey(Visiteur, on_delete=SET_NULL, null=True)
    visit = ForeignKey(VisiteurJourney, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True


class BaseUserModelVisited(BaseModelVisited):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    visit = ForeignKey(UsersJourney, on_delete=SET_NULL, null=True)
    
    class Meta:
        abstract = True


class VisiteurCompanyVisited(BaseVisiteurModelVisited):
    model_visited = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company visited by visiteur"
        db_table = "seo_companies_visited_visiteurs"
    

class UserCompanyVisited(BaseUserModelVisited):
    model_visited = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company visited by user"
        db_table = "seo_companies_visited_users"


class VisiteurPublicBlogVisited(BaseVisiteurModelVisited):
    model_visited = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog visited by visiteur"
        db_table = "seo_public_blogs_visited_visiteurs"
    

class UserPublicBlogVisited(BaseUserModelVisited):
    model_visited = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog visited by user"
        db_table = "seo_public_blogs_visited_users"


class VisiteurQuestionVisited(BaseVisiteurModelVisited):
    model_visited = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question visited by visiteur"
        db_table = "seo_questions_visited_visiteurs"
    

class UserQuestionVisited(BaseUserModelVisited):
    model_visited = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question visited by user"
        db_table = "seo_questions_visited_users"


class VisiteurTermVisited(BaseVisiteurModelVisited):
    model_visited = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term visited by visiteur"
        db_table = "seo_terms_visited_visiteurs"
    

class UserTermVisited(BaseUserModelVisited):
    model_visited = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term visited by user"
        db_table = "seo_terms_visited_users"
