from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    Textarea
) 

class NewsletterForm(ModelForm):
    class Meta:
        exclude = ['sent']