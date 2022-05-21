from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Factory

from apps.public_blog.models import PublicBlog

faker = Factory.create()


class PublicBlogFactory(DjangoModelFactory):

    class Meta:
        model = PublicBlog 