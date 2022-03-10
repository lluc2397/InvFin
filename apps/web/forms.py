from django.forms import (
    Form,
    CharField,
    EmailField,
    Textarea
) 

class ContactForm(Form):
    name = CharField(label='Nombre', required=True)
    email = EmailField(label='Email', required=True)
    message = CharField(widget=Textarea, label='Mensaje', required=True)

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']
        print(name)
        print(email)
        print(message)
        pass