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


class PosterTest(TestCase):
    def setUp(self) -> None:
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
        company_poster = SocialPosting(CompanySharedHistorial, company).generate_content()
        company_new_poster = SocialPosting(NewsSharedHistorial, company_related=company).generate_content()
        term_poster = SocialPosting(TermSharedHistorial, term).generate_content()
        blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
        question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()