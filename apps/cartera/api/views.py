from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic.edit import BaseFormView
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


class DefaultCreationView(LoginRequiredMixin, BaseFormView):
    template_name = 'cartera/modals/main_modals.html'
    success_message = 'Guardado correctamente'

    def get_success_url(self) -> str:
        return self.request.META.get('HTTP_REFERER')
    
    def successful_return(self):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
    
    def form_valid(self, form):
        form.save(self.request)
        return self.successful_return()


class AddDefaultCurrencyView(DefaultCreationView):
    form_class = DefaultCurrencyForm


class AddCashflowMoveView(DefaultCreationView):
    form_class = CashflowMoveForm


class AddPositionMovementView(DefaultCreationView):
    form_class = PositionMovementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # pass the 'user' in kwargs
        return kwargs


class AddCategoriesView(DefaultCreationView):
    form_class = AddCategoriesForm


class AddFinancialObjectifView(DefaultCreationView):
    form_class = FinancialObjectifForm


class AddNewAssetView(DefaultCreationView):
    form_class = AddNewAssetForm

    def form_valid(self, form):
        empresa_ticker = self.request.POST['stock'].split(' [')[1]
        ticker = empresa_ticker[:-1]
        empresa_busqueda = Company.objects.get(ticker = ticker)
        form.save(self.request, empresa_busqueda)
        return HttpResponseRedirect(self.get_success_url())


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