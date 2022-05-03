from django.forms import (
    BooleanField,
    DateInput,
    ModelForm,
    ChoiceField,
    Textarea,
    ModelChoiceField,
    ValidationError,
    ModelForm,
    Form,
    CharField,
    DecimalField,
    DateField,
    IntegerField
)

import datetime

from .models import (
    Income,
    Spend,
    PositionMovement,
    CashflowMovementCategory,
    FinancialObjectif,
    Asset
)

from apps.general.models import Currency


class BaseAssetMoveForm(Form):
    price = DecimalField(label='Precio unitario')
    date = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'id':'datepicker'}))
    quantity = IntegerField(label='Cantidad')
    currency = ModelChoiceField(label='Divisa', queryset=Currency.objects.all())
    observacion = CharField(widget=Textarea, required=False, label='Descripción')
    fee = DecimalField(label='Tarifa')

class AddNewAssetForm(BaseAssetMoveForm):    
    def save(self, request, company):
        model = super().save()
        model.is_stock = True
        model.user = request.user
        model.object = company
        model.save()
        request.user.user_patrimoine.assets.add(model)
        request.user.user_patrimoine.save()
        return model


class PositionMovementForm(ModelForm, BaseAssetMoveForm):
    move_type = ChoiceField(choices=[(1, 'Compra'), (2, 'Venta')], label='Moviemiento')
    asset_related = ModelChoiceField(queryset=Asset.objects.none())

    def __init__(self, user, *args, **kwargs):
        super(PositionMovementForm, self).__init__(*args, **kwargs)
        if user.is_authenticated:
            qs = Asset.objects.filter(user=user)
            self.fields['asset_related'].queryset = qs
        super(BaseAssetMoveForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PositionMovement
        exclude = ['user']
    
    def save(self, request):
        model = super().save()
        model.user = request.user
        model.save()
        return model


class FinancialObjectifForm(ModelForm):
    date_to_achieve = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'id':'datepicker'}))

    class Meta:
        model = FinancialObjectif
        fields = [
            'name',
            'date_to_achieve',
            'observation',
            'percentage',
            'amount',
        ]
    
    def save(self, request):
        model = super().save()
        model.user = request.user
        model.save()
        request.user.user_patrimoine.objectives.add(model)
        request.user.user_patrimoine.save()
        return model


class AddCategoriesForm(ModelForm):
    name = CharField(label='Nombre')

    class Meta:
        model = CashflowMovementCategory
        fields = ['name']
    
    def save(self, request):
        model = super().save()
        model.user = request.user
        model.save()
        return model


class DefaultCurrencyForm(Form):
    currency = ModelChoiceField(label='Divisa', queryset=Currency.objects.all())

    def save(self, user):
        user.user_patrimoine.default_currency = self.cleaned_data['currency']
        user.user_patrimoine.save()


class CashflowMoveForm(Form):
    move_type = ChoiceField(choices=[(0, 'Ingreso'), (1, 'Gasto')], label='Moviemiento')
    name = CharField(label='Nombre')
    amount = DecimalField(label='Cantidad')
    description = CharField(widget=Textarea, required=False, label='Descripción')
    date = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'id':'datepicker'}))
    currency = ModelChoiceField(label='Divisa', queryset=Currency.objects.all())
    is_recurrent = BooleanField(label='¿Es recurrente?', required=False)

    def save(self, request):
        name = self.cleaned_data['name']
        amount = self.cleaned_data['amount']
        description = self.cleaned_data['description']
        date = self.cleaned_data['date']
        currency = self.cleaned_data['currency']
        is_recurrent = self.cleaned_data['is_recurrent']

        if self.cleaned_data['move_type'] == '0':
            model = Income.objects
        else:
            model = Spend.objects

        model.create(
            user = request.user,
            name = name,
            amount = amount,
            description = description,
            date = date,
            currency = currency,
            is_recurrent = is_recurrent,
        )
        return model
