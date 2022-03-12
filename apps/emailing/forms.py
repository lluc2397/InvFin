from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    Form,
    Textarea
) 
from ckeditor.widgets import CKEditorWidget

class DefaultNewsletterFieldsForm(Form):
    title = CharField()
    intro = CharField(widget=CKEditorWidget(config_name='simple'))
    despedida = CharField(widget=CKEditorWidget(config_name='simple'))


class NewsletterForm(ModelForm):
    class Meta:
        exclude = ['sent']