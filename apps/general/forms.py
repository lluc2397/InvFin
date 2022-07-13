from ckeditor.widgets import CKEditorWidget
from django.forms import CharField, DateTimeField, Form, ModelForm, Textarea


class DefaultNewsletterForm(Form):
    title = CharField()
    content = CharField(widget=CKEditorWidget(config_name='writter'))
    date_to_send = DateTimeField()

    def annotate_changes(self, user):
        title = self.fields['title']
        intro = self.fields['intro']
        despedida = self.fields['despedida']
        if title.has_changed:
            print(title.initial)
            print('*'*100)
            print(title)
        if intro.has_changed:
            print('si')
        if despedida.has_changed:
            print('si')   

    def creating_newsletter(self, newsletter_model):
        title = self.cleaned_data['title']
        intro = self.cleaned_data['intro']
        despedida = self.cleaned_data['despedida']
        content = self.cleaned_data['content']
        date_to_send = self.cleaned_data['date_to_send']
        newsletter = newsletter_model.objects.create(
            title = title,
            introduction = intro,
            despedida = despedida,
            content = content,
            date_to_send = date_to_send,
        )
        return newsletter

    def send_email(self, newsletter_model):
        newsletter = self.creating_newsletter(newsletter_model)

        return newsletter.for_task