from typing import Any, Sequence
from factory import SubFactory
from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory

from apps.users.models import Profile

class UserFactory(DjangoModelFactory):
    id = 1
    username = 'Lucas'
    email = 'test@example.com'
    name = 'Lucas Montes'

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["id"]


class ProfileFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)

    class Meta:
        model = Profile