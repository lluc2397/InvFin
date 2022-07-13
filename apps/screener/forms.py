from django import forms

from .models import UserCompanyObservation


class UserCompanyObservationForm(forms.ModelForm):
    observation = forms.CharField(
        label="Describe tu observación",
        widget=forms.Textarea(attrs={'id':'observation'})
        )

    class Meta:
        model = UserCompanyObservation
        fields = [
            'observation',
            'observation_type'
        ]
        labels = {
            "observation_type": ("Elige la categoría")
        }