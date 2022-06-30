from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from apps.empresas.models import Company

from ..forms import (
    CashflowMoveForm,
    DefaultCurrencyForm,
    AddCategoriesForm,
    FinancialObjectifForm,
    AddNewAssetForm,
    PositionMovementForm
)


class BaseFinancialFormView(LoginRequiredMixin, FormView):
    success_message = 'Guardado correctamente'

    def successful_return(self):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponse(status=204, headers={'HX-Trigger': 'showMessageSuccess'})

    def form_valid(self, form):
        form.save(self.request)
        return self.successful_return()


class CurrencyInitial(BaseFinancialFormView):
    def get_initial(self):
        initial = super().get_initial()
        initial['currency'] = self.request.user.user_patrimoine.default_currency
        return initial


class AddDefaultCurrencyView(CurrencyInitial):
    template_name = 'cartera/modals/default_currency.html'
    form_class = DefaultCurrencyForm


class AddCashflowMoveView(CurrencyInitial):
    template_name = 'cartera/modals/cashflowmoves.html'
    form_class = CashflowMoveForm


class AddPositionMovementView(CurrencyInitial):
    template_name = 'cartera/modals/asset_movement.html'
    form_class = PositionMovementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AddCategoriesView(BaseFinancialFormView):
    template_name = 'cartera/modals/categories.html'
    form_class = AddCategoriesForm


class AddFinancialObjectifView(BaseFinancialFormView):
    template_name = 'cartera/modals/objectives.html'
    form_class = FinancialObjectifForm


class AddNewAssetView(CurrencyInitial):
    template_name = 'cartera/modals/new_asset.html'
    form_class = AddNewAssetForm

    def form_valid(self, form):
        empresa_ticker = self.request.POST['stock'].split(' [')[1]
        ticker = empresa_ticker[:-1]
        empresa_busqueda = Company.objects.get(ticker = ticker)
        form.save(self.request, empresa_busqueda)
        return self.successful_return()


@login_required(login_url='login')
def DeleteMove(request, id):
    user = request.user
    cartera = PATRIMONIO.objects.get(usuario =user)
    MOVIMIENTO.objects.get(id=id).delete()
    moves_user = MOVIMIENTO.objects.filter(user = user)
    if len(moves_user) == 0:
        for position in cartera.holds.all():
            position.delete()
        
    messages.success(request, f'Borrado correctamente')            
    return redirect(request.META.get('HTTP_REFERER'))