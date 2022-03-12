from django.forms import (
    ModelForm,
    ChoiceField,
    CharField,
    Form
)
from .models import WritterProfile, PublicBlog


class WritterProfileForm(ModelForm):

    class Meta:
        model = WritterProfile
        fields = [
            'long_description',
            'facebook',
            'twitter',
            'insta',
            'youtube',
            'linkedin',
            'tiktok',
        ]


class PublicBlogForm(ModelForm):
    STATUS = ((1, 'Publicar'), (2, 'Guardar como borrador'), (3, 'Programar'))

    status = ChoiceField(choices=STATUS)

    class Meta:
        model = PublicBlog
        fields = [
            'title',
            'resume',
            'status',
            'send_as_newsletter',
            'content'
        ]
        labels = {
            'title':('Título'),
            'resume':('Resumen'),
            'status':('Estatus'),
            'send_as_newsletter':('¿Quieres enviar este escrito como newsletter?'),
            'content':('Cuerpo')}
