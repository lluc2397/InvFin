from django import forms
from .models import (
    UserCompanyObservation
)

class UserCompanyObservationForm(forms.ModelForm):

    class Meta:
        model = UserCompanyObservation
        exclude = [
            'user',
            'company',
            'date',
]