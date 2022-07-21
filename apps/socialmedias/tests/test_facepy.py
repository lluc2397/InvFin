import vcr

from django.conf import settings
from django.test import TestCase

from apps.empresas.models import Company
from apps.escritos.models import Term, TermContent
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.constants import FACEBOOK
from apps.socialmedias.socialposter.facepy import Facebook

from ..poster import SocialPosting
from .data import AAPL, TERM, TERM_CONTENT, QUESTION, PUBLICBLOG
from .factories import DefaultTilteFactory, EmojiFactory, HashtagFactory


arrivalguides_vcr = vcr.VCR(
    cassette_library_dir='cassettes/arrivalguides/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class FacePosterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.facebook_poster = Facebook(settings.NEW_FACEBOOK_ID, settings.NEW_FB_PAGE_ACCESS_TOKEN)
        cls.question = Question.objects.create(**QUESTION)
        cls.term = Term.objects.create(**TERM)
        cls.term_content = TermContent.objects.create(**TERM_CONTENT)
        cls.public_blog = PublicBlog.objects.create(**PUBLICBLOG)
        cls.company = Company.objects.create(**AAPL)

    def test_blog(self):
        publicBlog = PublicBlog.objects.get_random()
        blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
        blog_response = publicBlog.title, 'https://inversionesyfinanzas.xyz' + publicBlog.get_absolute_url(), publicBlog.resume, 'https://inversionesyfinanzas.xyz' + publicBlog.image
        self.assertEqual(blog_poster, blog_response)

    def test_question(self):
        question = Question.objects.get_random()
        question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()
        print(question_poster)
        question_response= question.title, 'https://inversionesyfinanzas.xyz' + question.get_absolute_url(), question.content, None
        self.assertEqual(question_poster, question_response)

    def test_term(self):
        term = Term.objects.get_random()
        term_poster = SocialPosting(TermSharedHistorial, term).generate_content()
        term_response = term.title, 'https://inversionesyfinanzas.xyz' + term.get_absolute_url(), term.resume, 'https://inversionesyfinanzas.xyz' + term.image
        self.assertEqual(term_poster, term_response)

    def test_company(self):
        company = Company.objects.get_random()
        company_poster = SocialPosting(CompanySharedHistorial, company).generate_content()
        company_response = company.name, 'https://inversionesyfinanzas.xyz' + company.get_absolute_url(), company.description, company.image
        self.assertEqual(company_poster, company_response)
        title, link, description, media_url = company_poster
        print(description)
        
    def test_news(self):
        company = Company.objects.create(**AAPL)
        title, link, description, media_url = SocialPosting(NewsSharedHistorial, company_related=company).generate_content()
        
    # def test_posting(self):
    #     fb_response = self.facebook_poster.post_on_facebook(title=title, caption=description, post_type=3, link=link, media_url=media_url)
    #     print(fb_response)