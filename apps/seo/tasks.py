from config import celery_app

from .models import (
    VisiteurJourney, 
    UsersJourney,

    VisiteurCompanyVisited,
    VisiteurPublicBlogVisited,
    VisiteurQuestionVisited,
    VisiteurTermVisited,
    UserPublicBlogVisited,
    UserTermVisited,
    UserCompanyVisited,
    UserQuestionVisited,
)


@celery_app.task()
def post_promotion():
    pass


@celery_app.task()
def clean_visiteurs_journeys():
    for journey in VisiteurJourney.objects.filter(parsed=False):
        if journey.path == '':
            VisiteurCompanyVisited.objects.create()
        elif journey.path == '':
            VisiteurPublicBlogVisited.objects.create()
        elif journey.path == '':
            VisiteurQuestionVisited.objects.create()
        elif journey.path == '':
            VisiteurTermVisited.objects.create()
        journey.parsed = True
        journey.save(update_fields=['parsed'])


@celery_app.task()
def clean_users_journeys():
    for journey in VisiteurJourney.objects.filter(parsed=False):
        if journey.path == '':
            UserPublicBlogVisited.objects.create()
        elif journey.path == '':
            UserTermVisited.objects.create()
        elif journey.path == '':
            UserCompanyVisited.objects.create()
        elif journey.path == '':
            UserQuestionVisited.objects.create()
        journey.parsed = True
        journey.save(update_fields=['parsed'])
