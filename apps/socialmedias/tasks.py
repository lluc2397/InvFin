from config import celery_app

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
    SocialPosting(CompanySharedHistorial).share_content()


@celery_app.task()
def socialmedia_share_news():
    SocialPosting(NewsSharedHistorial).share_content()


@celery_app.task()
def socialmedia_share_term():
    SocialPosting(TermSharedHistorial).share_content()


@celery_app.task()
def socialmedia_share_blog():
    SocialPosting(BlogSharedHistorial).share_content()


@celery_app.task()
def socialmedia_share_question():
    SocialPosting(QuestionSharedHistorial).share_content(post_type=2)

