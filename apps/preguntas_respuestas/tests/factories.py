from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Factory

from apps.preguntas_respuestas.models import (
    Question,
    Answer,
    QuesitonComment,
    AnswerComment
)


faker = Factory.create()


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer


class QuesitonCommentFactory(DjangoModelFactory):
    class Meta:
        model = QuesitonComment


class AnswerCommentFactory(DjangoModelFactory):
    class Meta:
        model = AnswerComment
