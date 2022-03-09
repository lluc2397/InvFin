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

from apps.general.models import BasicWrittenContent, BaseComment, BaseContentShared
from ckeditor.fields import RichTextField

from apps.general.mixins import CommonMixin

class Question(BasicWrittenContent):
    content = RichTextField(config_name='simple')
    is_answered = BooleanField(default=False)
    has_accepted_answer = BooleanField(default=False)
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_question")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_question")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Question"
        db_table = "questions"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("preguntas_respuestas:question", kwargs={"slug": self.slug})
    
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


class Answer(CommonMixin):
    author = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='answers_apported') 
    created_at = DateTimeField(auto_now_add=True)
    content = RichTextField(config_name='simple')    
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


class QuestionSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        Question,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'questions_shared')

    class Meta:
        verbose_name = "Question shared"
        db_table = "shared_questions"