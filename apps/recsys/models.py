from django.db.models import (
    Model,
    JSONField,
    SET_NULL,
    ForeignKey,
    BooleanField,
    CharField
)
from django.contrib.auth import get_user_model

from apps.general.bases import BaseGenericModels
from apps.seo import constants
from apps.seo.models import VisiteurJourney, UsersJourney, Visiteur
from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog

User = get_user_model()


class BaseModelRecommended(BaseGenericModels):
    EXPLANATION = {
        'tags': [],
        'categories': [], 
    }
    place = CharField(max_length=150, choices=constants.WEP_PROMOTION_LOCATION)
    kind = CharField(max_length=150, choices=constants.WEP_PROMOTION_TYPE)
    clicked = BooleanField(default=False)
    recommendation_personalized = BooleanField(default=False)
    recommendation_explained = JSONField(default=dict)

    class Meta:
        abstract = True
    
    def __str__(self) -> str:
        try:
            response = self.user.username
        except:
            response = f'Visiteur - {self.user.id}'
        return response
    
    """
    Sobre escribir método clean o full clean. Cojer los motivos de la personalización o de la recomendación y guardalos en el json.
    """
    
    def full_clean(self, *args, **kwargs):
        return super().full_clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class BaseVisiteurModelRecommended(BaseModelRecommended):
    user = ForeignKey(Visiteur, on_delete=SET_NULL, null=True)
    visit = ForeignKey(VisiteurJourney, on_delete=SET_NULL, null=True)

    class Meta:
        abstract = True


class BaseUserModelRecommended(BaseModelRecommended):
    user = ForeignKey(User, on_delete=SET_NULL, null=True)
    visit = ForeignKey(UsersJourney, on_delete=SET_NULL, null=True)
    
    class Meta:
        abstract = True


class VisiteurCompanyRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company visited by visiteur"
        db_table = "recsys_companies_recommended_visiteurs"
    

class UserCompanyRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Company, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Company visited by user"
        db_table = "recsys_companies_recommended_users"


class VisiteurPublicBlogRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog visited by visiteur"
        db_table = "recsys_public_blogs_recommended_visiteurs"
    

class UserPublicBlogRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(PublicBlog, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "PublicBlog visited by user"
        db_table = "recsys_public_blogs_recommended_users"


class VisiteurQuestionRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question visited by visiteur"
        db_table = "recsys_questions_recommended_visiteurs"
    

class UserQuestionRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Question, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Question visited by user"
        db_table = "recsys_questions_recommended_users"


class VisiteurTermRecommended(BaseVisiteurModelRecommended):
    model_recommended = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term visited by visiteur"
        db_table = "recsys_terms_recommended_visiteurs"
    

class UserTermRecommended(BaseUserModelRecommended):
    model_recommended = ForeignKey(Term, on_delete=SET_NULL, null=True)

    class Meta:
        verbose_name = "Term visited by user"
        db_table = "recsys_terms_recommended_users"