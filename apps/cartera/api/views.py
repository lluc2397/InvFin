from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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


class DefaultCreationView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    success_message = 'Guardado correctamente'

    def get_success_url(self) -> str:
        return self.request.META.get('HTTP_REFERER')
    
    def form_valid(self, form):
        form.save(self.request)
        return super().form_valid(form)


class AddDefaultCurrencyView(DefaultCreationView):
    form_class = DefaultCurrencyForm


class AddCashflowMoveView(DefaultCreationView):
    form_class = CashflowMoveForm


class AddPositionMovementView(DefaultCreationView):
    form_class = PositionMovementForm

    def get_form_kwargs(self):
        kwargs = super(AddPositionMovementView, self).get_form_kwargs()
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