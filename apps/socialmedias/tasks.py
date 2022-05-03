from config import celery_app

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.empresas.models import Company

from .poster import SocialPosting
from .models import (
    CompanySharedHistorial,
    BlogSharedHistorial,
    NewsSharedHistorial,
    TermSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial
)

@celery_app.task()
def socialmedia_share_company():
    
    SocialPosting(CompanySharedHistorial, Company).share_content()


@celery_app.task()
def socialmedia_share_news():
    SocialPosting(NewsSharedHistorial, Company).share_content()


@celery_app.task()
def socialmedia_share_term():
    SocialPosting(TermSharedHistorial, Term).share_content()


@celery_app.task()
def socialmedia_share_blog():
    SocialPosting(BlogSharedHistorial, PublicBlog).share_content()


@celery_app.task()
def socialmedia_share_question():
    SocialPosting(QuestionSharedHistorial, Question).share_content(post_type=2)

