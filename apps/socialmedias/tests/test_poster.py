from django.test import TestCase
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)

from ..poster import SocialPosting
from .factories import DefaultTilteFactory, EmojiFactory, HashtagFactory

# from apps.public_blog.tests.factories




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
            content='<div><p>masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds</p> <a>sdfjhfb  fusd fvgsvd fsvd <a/></div>',
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
    
    def test_blog(self):
        publicBlog = PublicBlog.objects.get_random()
        blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
        blog_response = publicBlog.title, 'https://inversionesyfinanzas.xyz' + publicBlog.get_absolute_url(), publicBlog.resume
        self.assertEqual(blog_poster, blog_response)

    def test_question(self):
        question = Question.objects.get_random()
        question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()
        question_response= question.title, 'https://inversionesyfinanzas.xyz' + question.get_absolute_url(), question.content
        self.assertEqual(question_poster, question_response)

    def test_term(self):
        term = Term.objects.get_random()
        term_poster = SocialPosting(TermSharedHistorial, term).generate_content()
        term_response = term.title, 'https://inversionesyfinanzas.xyz' + term.get_absolute_url(), term.resume
        self.assertEqual(term_poster, term_response)

    def test_company(self):
        company = Company.objects.get_random()
        company_poster = SocialPosting(CompanySharedHistorial, company).generate_content()
        company_response = company.name, 'https://inversionesyfinanzas.xyz' + company.get_absolute_url(), company.description
        self.assertEqual(company_poster, company_response)

    def test_clean_description(self):
        title, link, description = SocialPosting(QuestionSharedHistorial, self.question).generate_content()
        description = strip_tags(description)
        self.assertEqual(description, 'masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds sdfjhfb  fusd fvgsvd fsvd ')
