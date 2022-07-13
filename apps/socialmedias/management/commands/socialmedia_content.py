from django.core.management import BaseCommand
from django.db import connection

from apps.socialmedias.models import DefaultTilte, Emoji, Hashtag

IG_HASHTAGS = ["valueinvestor", "valueinvesting", "invertirenvenezuela", "invertirencolombia", "invertirenespaña", "invertirmejor®", 
 "ingresospasivos", "inversionista", "inversionesinteligente", "bolsas", "inversión"]

FB_HASHTAGS = ["valueinvesting", "InvertirMejorQueAhorrar", "invertientufuturo", "inversionchallenge", "inversionista", "inversionesinteligentes", 
 "bolsa", "invertirenbolsa", "invertirmejor", 
 "inversiones", "invertir", "bolsadevalores", "invertirbien", "inversion", "invertironline"]

ICONS = ['😀',
 '😃',
 '😄',
 '😁',
 '😆',
 '😅',
 '😂',
 '🤣',
 '\U0001f972',
 '☺️',
 '😊',
 '😇',
 '🙂',
 '🙃',
 '😉',
 '😌',
 '😍',
 '🥰',
 '😘',
 '😗',
 '😙',
 '😚',
 '😋',
 '😛',
 '😝',
 '😜',
 '🤪',
 '🤨',
 '🧐',
 '🤓',
 '😎',
 '\U0001f978',
 '🤩',
 '🥳',
 '😏',
 '😒',
 '😞',
 '😔',
 '😟',
 '😕',
 '🙁',
 '☹️',
 '😣',
 '😖',
 '😫',
 '😩',
 '🥺',
 '😢',
 '😭',
 '😤',
 '😠',
 '😡',
 '🤬',
 '🤯',
 '😳',
 '🥵',
 '🥶',
 '😱',
 '😨',
 '😰',
 '😥',
 '😓',
 '🤗',
 '🤔',
 '🤭',
 '🤫',
 '🤥',
 '😶',
 '😐',
 '😑',
 '💸',
 '💵',
 '💴',
 '💶',
 '💷',
 '\U0001fa99',
 '💰',
 '💳',
 '💎',
 '⚖️',
 '\U0001fa9c',
 '🧰',
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
        

