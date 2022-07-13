from django.test import RequestFactory
from rest_framework import status
from rest_framework.test import APITestCase

from apps.empresas.tests.factories import CompanyFactory
from apps.seo.tasks import clean_journeys
from apps.users.tests.factories import UserFactory


class SEOTest(APITestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_parse_paths(self):
        clean_journeys()