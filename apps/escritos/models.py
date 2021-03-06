from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveIntegerField,
    TextField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from apps.general.bases import BaseComment, BaseEscrito, BaseFavoritesHistorial

from .managers import TermManager

DOMAIN = Site.objects.get_current().domain
User = get_user_model()

class Term(BaseEscrito):
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_term")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_term")
    # contributors = ManyToManyField(User, blank=True, related_name="contributors")
    objects = TermManager()

    class Meta:
        verbose_name = "Término del glosario"
        db_table = "term"
        ordering = ['id']
    
    def get_absolute_url(self):
        return reverse("escritos:single_term", kwargs={"slug": self.slug})
    
    @property
    def term_parts(self):
        return TermContent.objects.filter(term_related= self)
    
    def link(self):
        return f'https://{DOMAIN}{self.get_absolute_url()}'


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
        return f'{self.title}'
    
    def get_absolute_url(self):
        slug = slugify(self.title)
        path = self.term_related.get_absolute_url()
        return f'{path}#{slug}'
    
    def link(self):
        return f'https://{DOMAIN}{self.get_absolute_url()}'


class TermCorrection(Model):
    term_content_related = ForeignKey(TermContent,null = True, blank=True, on_delete=SET_NULL)
    title = CharField(max_length=3000,null = True, blank=True)
    date_suggested = DateTimeField(default=timezone.now)
    is_approved = BooleanField(default=False)
    date_approved = DateTimeField(blank=True, null=True)
    content = RichTextField(config_name='writter')
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
        return f'{self.term_content_related.title} corregido por {self.reviwed_by.username}'
    
    def save(self, *args, **kwargs): # new
        if self.is_approved is True:
            # Perfil.ADD_CREDITS(self.user, 5)
            #enviar email de agradecimiento
            pass
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return self.term_content_related.get_absolute_url()


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


class FavoritesTermsHistorial(BaseFavoritesHistorial):
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