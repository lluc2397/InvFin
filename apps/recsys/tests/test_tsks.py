from rest_framework import status
from rest_framework.test import APITestCase

from django.test import RequestFactory

from apps.users.tests.factories import UserFactory
from apps.empresas.tests.factories import CompanyFactory


from ..tasks import clean_journeys


class RecsysTest(APITestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_parse_paths(self):
        clean_journeys()