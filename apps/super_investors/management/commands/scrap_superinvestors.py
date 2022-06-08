from django.core.management import BaseCommand
from django.db import connection

from apps.super_investors.models import SuperinvestorActivity
from apps.super_investors.scrapper import get_historial


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        for superinvestor in SuperinvestorActivity.objects.all():
            get_historial(superinvestor)
        

