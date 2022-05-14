from django.test import TestCase

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.empresas.models import Company

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
        self.hashtag = HashtagFactory()

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

    def test_random_content(self):
        random_Term_1 = Term.objects.get_random()
        random_Question_1 = Question.objects.get_random()
        random_PublicBlog_1 = PublicBlog.objects.get_random()
        random_Company_1 = Company.objects.get_random()

        random_Term_2 = Term.objects.get_random()
        random_Question_2 = Question.objects.get_random()
        random_PublicBlog_2 = PublicBlog.objects.get_random()
        random_Company_2 = Company.objects.get_random()

        if random_Term_1 == random_Term_2:
            self.assertEqual(random_Term_1, random_Term_2)
        else:
            self.assertNotEqual(random_Term_1, random_Term_2)
        if random_Question_1 == random_Question_2:
            self.assertEqual(random_Question_1, random_Question_2)
        else:
            self.assertNotEqual(random_Question_1, random_Question_2)
        if random_PublicBlog_1 == random_PublicBlog_2:
            self.assertEqual(random_PublicBlog_1, random_PublicBlog_2)
        else:
            self.assertNotEqual(random_PublicBlog_1, random_PublicBlog_2)
        if random_Company_1 == random_Company_2:
            self.assertEqual(random_Company_1, random_Company_2)
        else:
            self.assertNotEqual(random_Company_1, random_Company_2)

    def test_content_results(self):
        term = Term.objects.get_random()
        question = Question.objects.get_random()
        publicBlog = PublicBlog.objects.get_random()
        company = Company.objects.get_random()

        term_poster = SocialPosting(TermSharedHistorial, term).generate_content()
        blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
        question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()
        company_poster = SocialPosting(CompanySharedHistorial, company).generate_content()
        company_news_poster = SocialPosting(NewsSharedHistorial, company_related=company).generate_content()
        
        term_poster_json = term.title, 'https://inversionesyfinanzas.xyz' + term.get_absolute_url(), term.resume, term.image
        blog_poster_json = question.title, 'https://inversionesyfinanzas.xyz' + question.get_absolute_url(), question.content, None
        question_poster_json = publicBlog.title, 'https://inversionesyfinanzas.xyz' + publicBlog.get_absolute_url(), publicBlog.resume, publicBlog.image
        company_poster_json = company.name, 'https://inversionesyfinanzas.xyz' + company.get_absolute_url(), company.resume, company.image
        # company_new_poster_json = {}
        
        self.assertEqual(term_poster, term_poster_json)
        self.assertEqual(blog_poster, blog_poster_json)
        self.assertEqual(question_poster, question_poster_json)
        self.assertEqual(company_poster, company_poster_json)
        # self.assertEqual(company_news_poster, company_new_poster_json)
    
    def test_posting(self):
        question = Question.objects.get_random()
        question_poster = SocialPosting(QuestionSharedHistorial, question).share_content(3)
        print(question_poster)