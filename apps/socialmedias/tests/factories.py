from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.socialmedias.models import (
    Emoji,
    DefaultTilte,
    Hashtag
)


class EmojiFactory(DjangoModelFactory):
    emoji = '😀'
    class Meta:
        model = Emoji


class DefaultTilteFactory(DjangoModelFactory):
    title = 'No te lo pierdas'
    class Meta:
        model = DefaultTilte


class HashtagFactory(DjangoModelFactory):
    name = 'test'
    class Meta:
        model = Hashtag

