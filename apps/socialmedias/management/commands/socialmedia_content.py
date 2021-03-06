from django.core.management import BaseCommand
from django.db import connection

from apps.socialmedias.models import DefaultTilte, Emoji, Hashtag

IG_HASHTAGS = ["valueinvestor", "valueinvesting", "invertirenvenezuela", "invertirencolombia", "invertirenespaรฑa", "invertirmejorยฎ", 
 "ingresospasivos", "inversionista", "inversionesinteligente", "bolsas", "inversiรณn"]

FB_HASHTAGS = ["valueinvesting", "InvertirMejorQueAhorrar", "invertientufuturo", "inversionchallenge", "inversionista", "inversionesinteligentes", 
 "bolsa", "invertirenbolsa", "invertirmejor", 
 "inversiones", "invertir", "bolsadevalores", "invertirbien", "inversion", "invertironline"]

ICONS = ['๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐คฃ',
 '\U0001f972',
 'โบ๏ธ',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐ฅฐ',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐คช',
 '๐คจ',
 '๐ง',
 '๐ค',
 '๐',
 '\U0001f978',
 '๐คฉ',
 '๐ฅณ',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 '๐',
 'โน๏ธ',
 '๐ฃ',
 '๐',
 '๐ซ',
 '๐ฉ',
 '๐ฅบ',
 '๐ข',
 '๐ญ',
 '๐ค',
 '๐ ',
 '๐ก',
 '๐คฌ',
 '๐คฏ',
 '๐ณ',
 '๐ฅต',
 '๐ฅถ',
 '๐ฑ',
 '๐จ',
 '๐ฐ',
 '๐ฅ',
 '๐',
 '๐ค',
 '๐ค',
 '๐คญ',
 '๐คซ',
 '๐คฅ',
 '๐ถ',
 '๐',
 '๐',
 '๐ธ',
 '๐ต',
 '๐ด',
 '๐ถ',
 '๐ท',
 '\U0001fa99',
 '๐ฐ',
 '๐ณ',
 '๐',
 'โ๏ธ',
 '\U0001fa9c',
 '๐งฐ',
 '\U0001fa9b']

TWITTER_HASHTAGS = ['invertir', 'inversiones', 'valueinvesting', 'invertirenvalor', 'inversionesinteligente',
    'bolsa', 'invertirenbolsa', 'inversorinteligente']


class Command(BaseCommand):

    def handle(self, *args, **options):
        ig = [Hashtag(
            name=hashtag,
            platform='instagram'
        ) for hashtag in IG_HASHTAGS]
        fb = [Hashtag(
            name=hashtag,
            platform='facebook'
        ) for hashtag in FB_HASHTAGS]
        tw = [Hashtag(
            name=hashtag,
            platform='twitter'
        ) for hashtag in TWITTER_HASHTAGS]
        emojis = [Emoji(emoji=emoji) for emoji in ICONS]
        hashtags = ig + tw + fb
        Hashtag.objects.bulk_create(hashtags)
        Emoji.objects.bulk_create(emojis)
        

