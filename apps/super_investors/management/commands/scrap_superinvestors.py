from django.core.management import BaseCommand
from django.db import connection

from apps.super_investors.models import Superinvestor, SuperinvestorActivity
from apps.super_investors.scrapper import get_activity


class Command(BaseCommand):

    def handle(self, *args, **options):
        SuperinvestorActivity.objects.all().delete()
        for superinvestor in Superinvestor.objects.all():
            get_activity(superinvestor)
        

