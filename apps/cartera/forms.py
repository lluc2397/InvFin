from django.forms import (
    BooleanField,
    DateInput,
    ModelForm,
    ChoiceField,
    Textarea,
    ModelChoiceField,
    ModelForm,
    Form,
    CharField,
    DecimalField,
    DateField,
    IntegerField
)
from django.contrib.auth import get_user_model

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

User = get_user_model()


class BaseForm(Form):
    currency = ModelChoiceField(label='Divisa', queryset=Currency.objects.all())


class BaseAssetMoveForm(BaseForm):
    price = DecimalField(label='Precio unitario')
    date = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'class':'datetimepicker1'}))
    quantity = IntegerField(label='Cantidad')
    observacion = CharField(widget=Textarea, required=False, label='Descripción')
    fee = DecimalField(label='Comisión', initial=0)


class AddNewAssetForm(ModelForm, BaseAssetMoveForm):
    class Meta:
        model = PositionMovement
        exclude = [
            'user',
            'move_type',
            'asset_related',
        ]

    def save(self, request, company):
        asset = Asset.objects.create(
            is_stock = True,
            user = request.user,
            object = company
        )

        position = super().save()
        position.user = request.user
        position.asset_related = asset
        position.move_type = 1
        position.save()

        request.user.user_patrimoine.assets.add(asset)
        request.user.user_patrimoine.save()
        return asset


class PositionMovementForm(ModelForm, BaseAssetMoveForm):
    move_type = ChoiceField(choices=[(1, 'Compra'), (2, 'Venta')], label='Movimiento')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PositionMovementForm, self).__init__(*args, **kwargs)
        self.fields['asset_related'].queryset = user.user_patrimoine.assets.all()
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
    widget = DateInput(attrs={'class':'datetimepicker1'}))

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


class DefaultCurrencyForm(BaseForm):
    def save(self, request):
        request.user.user_patrimoine.default_currency = self.cleaned_data['currency']
        request.user.user_patrimoine.save()


class CashflowMoveForm(BaseForm):
    move_type = ChoiceField(choices=[(0, 'Ingreso'), (1, 'Gasto')], label='Moviemiento')
    name = CharField(label='Nombre')
    amount = DecimalField(label='Cantidad')
    description = CharField(widget=Textarea, required=False, label='Descripción')
    date = DateField(label='Fecha', initial=datetime.date.today,
    widget = DateInput(attrs={'class':'datetimepicker1'}))
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
