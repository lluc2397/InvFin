from django.core.management import BaseCommand

from ...models import YahooScreener


class Command(BaseCommand):

    def handle(self, *args, **options):
        for screener in YahooScreener.objects.all():
            if YahooScreener.objects.filter(slug=screener.slug).exclude(pk=screener.pk).exists():
                screener.slug = f'{screener.slug}-1'
                screener.save(update_fields=['slug'])
