from django import forms

from .models import WritterProfile, PublicBlog

class WritterProfileForm(forms.ModelForm):

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


class PublicBlogForm(forms.ModelForm):

    class Meta:
        model = PublicBlog
        fields = [
            'title',
            'resume',
            'status',
            'content'
        ]
        labels = {
            'title':('Título'),
            'resume':('Resumen'),
            'status':('Estatus'),
            'content':('Cuerpo')}
