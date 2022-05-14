from django.test import TestCase

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.empresas.models import Company

from apps.socialmedias.socialposter.tweetpy import Twitter
from apps.socialmedias.models import (
    CompanySharedHistorial,
    BlogSharedHistorial,
    NewsSharedHistorial,
    TermSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial
)
from ..poster import SocialPosting

from .factories import (
    EmojiFactory,
    DefaultTilteFactory,
    HashtagFactory
)

class PosterTest(TestCase):
    def setUp(self) -> None:
        self.emoji = EmojiFactory()
        self.def_title = DefaultTilteFactory()
        self.hashtag = HashtagFactory(platform='twitter')
        self.hashtag2 = HashtagFactory(platform='twitter')
        self.hashtag3 = HashtagFactory(platform='twitter')

        self.term = Term.objects.create(
            title='term',
            resume='resumen',
        )
        self.question = Question.objects.create(
            title='question',
            content='pregutna larga',
        )
        self.publicBlog = PublicBlog.objects.create(
            title='public blog',
            resume='blog resumido',
            content='contenido largo del blog',
        )
        self.company = Company.objects.create(
            name='Apple',
            ticker='AAPL'
        )
        self.term2 = Term.objects.create(
            title='term 2',
            resume='resumen 2',
        )
        self.question2 = Question.objects.create(
            title='question 2',
            content='pregutna larga 2',
        )
        self.publicBlog2 = PublicBlog.objects.create(
            title='public blog 2',
            resume='blog resumido 2',
            content='contenido largo del blog 2',
        )
        self.company2 = Company.objects.create(
            name='Intel',
            ticker='INTC'
        )
    
    def test_post(self):
        question = Question.objects.get_random()
        title, link, description, media_url = SocialPosting(QuestionSharedHistorial, question).generate_content()

        tw_response = Twitter().tweet(caption=description, post_type=3, media_url=media_url, link=link)
        print(tw_response)