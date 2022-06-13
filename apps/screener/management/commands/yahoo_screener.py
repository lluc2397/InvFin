from django.core.management import BaseCommand
from django.template.defaultfilters import slugify

from ...models import YahooScreener
from ... import constants

from apps.translate.google_trans_new import google_translator
import yahooquery as yq

class Command(BaseCommand):

    def handle(self, *args, **options):
        yq_screener = yq.Screener()
        for screener in yq_screener.available_screeners:
            if YahooScreener.objects.filter(yq_name=screener).exists():
                continue
            if screener.startswith('all_cryptocurrencies'):
                asset_class_related = constants.CRYPTO
            elif screener.startswith('reit'):
                asset_class_related = constants.REIT
            elif screener.startswith('top_etfs'):
                asset_class_related = constants.ETF
            elif screener.startswith('top_mutual_funds'):
                asset_class_related = constants.MUTUAL_FUND
            else:
                asset_class_related = constants.STOCK
            try:
                screener_lookup = yq_screener.get_screeners(screener, 1)
                if screener_lookup[screener] == 'No screener records found. Check if scrIds are correct':
                    continue
                screener_lookup_info = screener_lookup[screener]

                name = screener_lookup_info['title'] 
                description = screener_lookup_info['description'] 

                name = google_translator().translate(name, lang_src='en', lang_tgt='es')
                description = google_translator().translate(description, lang_src='en', lang_tgt='es')
                slug = slugify(name)
                screener_search = YahooScreener.objects.filter(yq_name=screener)
                if screener_search.exists():
                    if screener_search.count()>1:
                        sc = screener_search.first()
                        sc.slug = f'{sc.slug}-{screener[-2:]}'
                    else:
                        continue
                else:
                    YahooScreener.objects.create(
                        name = name,
                        slug = slug,
                        description = description,
                        json_info = screener_lookup_info,
                        yq_name = screener,
                        asset_class_related = asset_class_related
                    )

                print(f'{screener} created')
            except Exception:
                pass
        print('Done')

# es.finance.yahoo.com