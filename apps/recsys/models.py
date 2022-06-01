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

from apps.seo import constants
from apps.seo.models import VisiteurJourney, UsersJourney
from apps.empresas.models import Company

User = get_user_model()


class CompanyShowed(Model):
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, related_name="shows")
    place = CharField(max_length=500, choices=constants.WEP_PROMOTION_LOCATION)
    start_date = DateTimeField(auto_now_add=True)
    end_date = DateTimeField(null=True, blank=True)


class CompanyMostVisited(Model):
    company = ForeignKey(Company, on_delete=SET_NULL, null=True, related_name="searchs")
    historial = JSONField(default=dict)


class VisiteurCompanyVisited(Model):
    visiteur = ''
    company_visited = ''
    date = ''


class UserCompanyVisited(Model):
    user = ''
    company_visited = ''
    date = ''