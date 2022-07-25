from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    JSONField,
    ManyToManyField,
    Model,
    PositiveBigIntegerField,
    SlugField,
    TextField,
)
from django.utils import timezone

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.constants import SOCIAL_MEDIAS

from . import constants

User = get_user_model()


# class URLHistorial(Model):
#     old_url
#     new_url

# from django.contrib.sessions.models import Session

class Visiteur(Model):
    ip = CharField(max_length=50, null=True, blank=True)
    session_id = CharField(max_length=1000, null=True, blank=True)
    HTTP_USER_AGENT = CharField(max_length=1000, null=True, blank=True)
    country_code = CharField(max_length=300, null=True, blank=True)
    country_name = CharField(max_length=300, null=True, blank=True)
    dma_code = CharField(max_length=300, null=True, blank=True)
    is_in_european_union = BooleanField(null=True, blank=True)
    latitude = CharField(max_length=300, null=True, blank=True)
    longitude = CharField(max_length=300, null=True, blank=True)
    city = CharField(max_length=500, null=True, blank=True)
    region = CharField(max_length=300, null=True, blank=True)
    time_zone = CharField(max_length=300, null=True, blank=True)
    postal_code = CharField(max_length=15, null=True, blank=True)
    continent_code = CharField(max_length=300, null=True, blank=True)
    continent_name = CharField(max_length=300, null=True, blank=True)
    first_visit_date = DateTimeField(auto_now_add=True)
    is_bot = BooleanField(default=False)

    class Meta:
        verbose_name = "Visiteur"
        db_table = "visiteurs"
    
    def __str__(self):
        return str(self.id)
    
    @property
    def app_label(self):
        return self._meta.app_label
    
    @property
    def object_name(self):
        return self._meta.object_name
    

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
    parsed = BooleanField(default=False)

    class Meta:
        abstract = True


class VisiteurJourney(Journey):
    user = ForeignKey(Visiteur, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas anónimos"
        db_table = "visits_historial_visiteurs"
    

class UserJourney(Journey):
    user = ForeignKey(User, null = True, blank=True, on_delete=CASCADE)

    class Meta:
        verbose_name = "Historial visitas usuarios"
        db_table = "visits_historial_users"


class VisiteurUserRelation(Model):
    user = ForeignKey(User, null = True, blank=True, on_delete=SET_NULL)
    visiteur = ForeignKey(Visiteur, null = True, blank=True, on_delete=SET_NULL)
    date = DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Relación usuarios visitantes"
        db_table = "seo_users_visiteurs_relation"


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
    visit = ForeignKey(UserJourney, on_delete=SET_NULL, null=True)
    
    class Meta:
        abstract = True


class VisiteurCompanyVisited(BaseVisiteurModelVisited):
    model_visited = ForeignKey(
        Company, 
        on_delete=SET_NULL, 
        null=True,
    )

    class Meta:
        verbose_name = "Company visited by visiteur"
        db_table = "seo_companies_visited_visiteurs"
    

class UserCompanyVisited(BaseUserModelVisited):
    model_visited = ForeignKey(
        Company, 
        on_delete=SET_NULL, 
        null=True,
    )

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
