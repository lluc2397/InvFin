from django.db.models import (
    Model,
    SET_NULL,
    CASCADE,
    ForeignKey,
    DateTimeField,
    BooleanField,
    IntegerField,
    ManyToManyField
)
from django.contrib.sites.models import Site
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from apps.general.models import BasicWrittenContent, BaseComment
from ckeditor.fields import RichTextField

from apps.general.mixins import CommonMixin

from itertools import chain

from .managers import QuestionManager

class Question(BasicWrittenContent):
    content = RichTextField(config_name='writter')
    is_answered = BooleanField(default=False)
    has_accepted_answer = BooleanField(default=False)
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_question")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_question")
    objects = QuestionManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        db_table = "questions"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("preguntas_respuestas:question", kwargs={"slug": self.slug})
    
    @property
    def related_users(self):
        answers_users = self.related_answers
        upvotes_users = self.upvotes.all()
        downvotes_users = self.downvotes.all()
        comments_users = self.comments_related.all()
        return list(chain(answers_users, upvotes_users, downvotes_users, comments_users))
    
    @property
    def related_answers(self):
        return self.question_answers.all()
    
    def add_answer(self, answer):
        Answer.objects.create(
            author = self.author,
            content = answer,
            question_related = self,
            is_accepted = True,
        )

    @property
    def ques_schema(self):
        ques_schema = {}
        ques_schema['@context'] = "https://schema.org"
        ques_schema['@type'] = "QAPage"
        ques_schema['mainEntity'] = {}
        ques_schema['mainEntity']["@type"] = "Question"
        ques_schema['mainEntity']["name"] = self.title
        ques_schema['mainEntity']["text"] = self.content
        ques_schema['mainEntity']["answerCount"] = self.related_answers.count()
        ques_schema['mainEntity']["upvoteCount"] = self.upvotes.all().count()
        ques_schema['mainEntity']["dateCreated"] = self.created_at
        ques_schema['mainEntity']["author"] = {}
        ques_schema['mainEntity']["author"]["@type"] = "Person"
        ques_schema['mainEntity']["author"]["name"] = self.author        
        
        ques_schema['mainEntity']["suggestedAnswer"] = []

        for answer in self.related_answers:
            if answer.is_accepted:
                ques_schema['mainEntity']["acceptedAnswer"] = {}
                ques_schema['mainEntity']["acceptedAnswer"]['@type'] = "Answer"
                ques_schema['mainEntity']["acceptedAnswer"]['text'] = answer.content
                ques_schema['mainEntity']["acceptedAnswer"]['dateCreated'] = answer.created_at
                ques_schema['mainEntity']["acceptedAnswer"]['upvoteCount'] = answer.total_votes
                ques_schema['mainEntity']["acceptedAnswer"]['url'] = answer.own_url
                ques_schema['mainEntity']["acceptedAnswer"]['author'] = {}
                ques_schema['mainEntity']["acceptedAnswer"]['author']['@type'] = "Person"
                ques_schema['mainEntity']["acceptedAnswer"]['author']['name'] = answer.author.full_name

            sug_answ = {}
            sug_answ['@type'] = "Answer"
            sug_answ['text'] = answer.content
            sug_answ['dateCreated'] = answer.created_at
            sug_answ['upvoteCount'] = answer.total_votes
            sug_answ['url'] = answer.own_url
            sug_answ['author'] = {}
            sug_answ['author']['@type'] = "Person"
            sug_answ['author']['name'] = answer.author.full_name
            ques_schema['mainEntity']["suggestedAnswer"].append(sug_answ)

        return ques_schema


class Answer(CommonMixin):
    author = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='answers_apported') 
    created_at = DateTimeField(auto_now_add=True)
    content = RichTextField(config_name='writter')    
    question_related = ForeignKey(
        Question,
        on_delete=CASCADE,
        blank=False,
        related_name = "question_answers")
    is_accepted = BooleanField(default=False)
    total_votes = IntegerField(default=0)
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_answer")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_answer")
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Answer"
        db_table = "answers"
    
    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return self.question_related.get_absolute_url()
    
    @property
    def own_url(self):
        domain = Site.objects.get_current().domain
        return f'https://{domain}/question/{self.question_related.slug}/#{self.id}'


class QuesitonComment(BaseComment):
    content_related = ForeignKey(Question,
        on_delete=CASCADE,
        null=True,
        related_name = "comments_related")

    class Meta:
        verbose_name = "Question's comment"
        db_table = "question_comments"
    
    def __str__(self):
        return str(self.id)


class AnswerComment(BaseComment):
    content_related = ForeignKey(Answer,
        on_delete=CASCADE,
        null=True,
        related_name = "comments_related")
    
    class Meta:
        verbose_name = "Answer's comment"
        db_table = "answer_comments"
    
    def __str__(self):
        return str(self.id)
