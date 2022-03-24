from django.forms import (
    BooleanField,
    DateInput,
    ModelForm,
    ChoiceField,
    Textarea,
    ValidationError,
    ModelForm,
    Form,
    CharField,
    DecimalField,
    DateField
)

import datetime

from .models import (
    Income,
    Spend,
    PositionMovement
)

from apps.general.models import Currency

class CashflowMoveForm(Form):
    move_type = ChoiceField(choices=[(0, 'Ingreso'), (1, 'Gasto')], label='Moviemiento')
    name = CharField(label='Nombre')
    amount = DecimalField(label='Cantidad')
    description = CharField(widget=Textarea, required=False, label='Descripción')
    date = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'id':'datepicker'}))
    currency = ChoiceField(label='Divisa', choices=[(currency.id, currency.currency) for currency in Currency.objects.all()])
    is_recurrent = BooleanField(label='¿Es recurrente?', required=False)

    def create_cashflow(self, user):
        name = self.cleaned_data['name']
        amount = self.cleaned_data['amount']
        description = self.cleaned_data['description']
        date = self.cleaned_data['date']
        currency = Currency.objects.get(id = self.cleaned_data['currency'])
        is_recurrent = self.cleaned_data['is_recurrent']

        if self.cleaned_data['move_type'] == '0':
            model = Income.objects
        else:
            model = Spend.objects

        model.create(
            user = user,
            name = name,
            amount = amount,
            description = description,
            date = date,
            currency = currency,
            is_recurrent = is_recurrent,
        )


class PositionMovementForm(ModelForm):
    user = ''
    move_type = ''
    asset_related = ''
    price = ''
    date = ''
    quantity = ''
    currency = ''
    observacion = ''
    fee = ''

    class Meta:
        model = PositionMovement
        exclude = ['user'] 
