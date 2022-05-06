from django.test import TestCase

from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.empresas.models import Company

from ..models import (
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
        self.company_poster = SocialPosting(CompanySharedHistorial, content_shared=Company).share_content(6)
        self.company_new_poster = SocialPosting(NewsSharedHistorial, company_related=Company).share_content(6)
        self.term_poster = SocialPosting(TermSharedHistorial, content_shared=Term).share_content(6)
        self.blog_poster = SocialPosting(BlogSharedHistorial, content_shared=PublicBlog).share_content(6)
        self.questio_poster = SocialPosting(QuestionSharedHistorial, content_shared=Question).share_content(3)

    