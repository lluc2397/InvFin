from django.test import TestCase

from apps.general.utils import NotificationSystem
from apps.empresas.company.update import UpdateCompany
from apps.empresas.tests.factories import CompanyFactory
from apps.public_blog.tests.factories import PublicBlogFactory
from apps.preguntas_respuestas.tests.factories import (
    QuestionFactory,
    AnswerFactory,
    QuesitonCommentFactory,
    AnswerCommentFactory
)
from .. import constants


class NotificationSystemTest(TestCase):
    def setUp(self) -> None:
        self.