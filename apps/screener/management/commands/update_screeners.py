from django.core.management import BaseCommand

from ...models import YahooScreener


class Command(BaseCommand):

    def handle(self, *args, **options):
        for screener in YahooScreener.objects.all():
            if YahooScreener.objects.filter(slug=screener.slug).exclude(pk=screener.pk).exists():
                YahooScreener.objects.create(
                    name=screener.name,
                    slug=f'{screener.slug}-1',
                    description=screener.description,
                    json_info=screener.json_info,
                    yq_name=screener.yq_name,
                    asset_class_related=screener.asset_class_related,
                    show=screener.show,
                )
                screener.delete()
