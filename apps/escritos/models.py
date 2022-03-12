from django.db.models import (
    Model,
    CharField,
    SET_NULL,
    CASCADE,
    ForeignKey,
    TextField,
    DateTimeField,
    BooleanField,
    PositiveIntegerField,
    OneToOneField,
    IntegerField,
    ManyToManyField
)

from ckeditor.fields import RichTextField

from django.urls import reverse
from django.utils import timezone

from apps.general.models import BaseEscrito, BaseComment, BaseContentShared, FavoritesHistorial

from django.contrib.auth import get_user_model
User = get_user_model()

class Term(BaseEscrito):
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_term")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_term")

    class Meta:
        verbose_name = "Término del glosario"
        db_table = "term"
        ordering = ['id']
    
    def get_absolute_url(self):
        return reverse("escritos:single_term", kwargs={"slug": self.slug})
    
    @property
    def term_parts(self):
        return TermContent.objects.filter(term_related= self)


class TermContent(Model):
    term_related = ForeignKey(Term, on_delete=SET_NULL, null=True, related_name="term_content_parts") 
    title = CharField(max_length=3000)
    order = PositiveIntegerField(default=0)
    content = RichTextField()

    class Meta:
        ordering = ['order']
        verbose_name = "Partes del término"
        db_table = "term_content"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("escritos:correction_term", kwargs={"id": self.id})


class TermCorrection(Model):
    term_content_related = ForeignKey(TermContent,null = True, blank=True, on_delete=CASCADE)
    title = CharField(max_length=3000,null = True, blank=True)
    date_suggested = DateTimeField(default=timezone.now)
    is_approved = BooleanField(default=False)
    date_approved = DateTimeField(default=timezone.now)
    content = RichTextField(config_name='simple')
    reviwed_by = ForeignKey(
        User,
        null = True,
        blank=True,
        related_name='corrector',
        on_delete=SET_NULL)

    approved_by = ForeignKey(
        User,
        null = True,
        blank=True,
        related_name='revisor',
        on_delete=SET_NULL)

    class Meta:
        ordering = ['id']
        verbose_name = "Corrections terms"
        db_table = "term_content_correction"

    def __str__(self):
        return self.term_content_related.title
    
    def save(self, *args, **kwargs): # new
        if self.is_approved is True:
            # Perfil.ADD_CREDITS(self.user, 5)
            #enviar email de agradecimiento
            pass
        return super().save(*args, **kwargs)


class TermsComment(BaseComment):
    content_related = ForeignKey(Term,
        on_delete=CASCADE,
        null=True,
        related_name = "comments_related")

    class Meta:
        verbose_name = "Term's comment"
        db_table = "term_comments"
    
    def get_absolute_url(self):
        return self.content_related.get_absolute_url()


class TermsRelatedToResume(Model):
    term_to_keep = ForeignKey(Term,
        on_delete=CASCADE,
        null=True,
        related_name = "term_to_keep")
        
    term_to_delete = ForeignKey(Term,
        on_delete=CASCADE,
        null=True,
        related_name = "term_to_delete")    
    
    class Meta:
        verbose_name = "Terms to resume"
        db_table = "terms_to_resume"


class TermSharedHistorial(BaseContentShared):
    content_shared = ForeignKey(
        Term,
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name = 'terms_shared')

    class Meta:
        verbose_name = "Term shared"
        db_table = "shared_terms"


class FavoritesTermsHistorial(FavoritesHistorial):
    term = ForeignKey(Term, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Término favorito"
        verbose_name_plural = "Términos favoritos"
        db_table = "favorites_terms_historial"

    def __str__(self):
        return f'{self.user.username}'


class FavoritesTermsList(Model):
    user = OneToOneField(User,on_delete=SET_NULL,null=True, blank=True, related_name="favorites_terms")
    term = ManyToManyField(Term, blank=True)

    class Meta:
        verbose_name = "Lista de términos favoritos"
        verbose_name_plural = "Lista de términos favoritos"
        db_table = "favorites_terms_list"

    def __str__(self):
        return self.user.username