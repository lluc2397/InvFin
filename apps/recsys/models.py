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

from apps.seo.models import VisiteurJourney, UsersJourney

User = get_user_model()


class VisiteurCompanyVisited(Model):
    visiteur = ''
    company = ''
    date = ''


class UserCompanyVisited(Model):
    user = ''
    company = ''
    date = ''