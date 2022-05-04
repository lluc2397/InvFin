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
    post_type = 6
    content_shared = Company
    SocialPosting(CompanySharedHistorial, 5).share_content(content_shared)


@celery_app.task()
def socialmedia_share_news():
    post_type = 6
    company_related = Company
    SocialPosting(NewsSharedHistorial, 2).share_content(company_related)


@celery_app.task()
def socialmedia_share_term():
    post_type = 3
    post_type = 6
    content_shared = Term
    SocialPosting(TermSharedHistorial, 3).share_content(content_shared)


@celery_app.task()
def socialmedia_share_blog():
    post_type = 3
    post_type = 6
    content_shared = PublicBlog
    SocialPosting(BlogSharedHistorial, 4).share_content(content_shared)


@celery_app.task()
def socialmedia_share_question():
    post_type = 3
    content_shared = Question
    SocialPosting(QuestionSharedHistorial, 1).share_content(content_shared)

