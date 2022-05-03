from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from apps.empresas.models import Company

from .models import (
	Patrimonio
)
from .forms import (
    CashflowMoveForm,
    DefaultCurrencyForm,
    AddCategoriesForm,
    FinancialObjectifForm,
    AddNewAssetForm,
    PositionMovementForm
)

User = get_user_model()


class InicioCarteraView(LoginRequiredMixin, TemplateView):
    template_name = "cartera/private/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patrimonio"] = Patrimonio.objects.get_or_create(user = self.request.user)[0]
        initial = {}
        if self.request.user.is_authenticated:
            initial['currency'] = self.request.user.user_patrimoine.default_currency
        context["cashflowform"] = CashflowMoveForm(initial=initial)
        context["defcurrencyform"] = DefaultCurrencyForm()

        context["asset_movement_form"] = PositionMovementForm(initial=initial, user=self.request.user)
        context["new_asset_form"] = AddNewAssetForm(initial=initial)

        context["add_categories_form"] = AddCategoriesForm()
        context["add_financial_objective_form"] = FinancialObjectifForm()
        context["meta_title"] = 'Tu gestor patrimonial'
        return context


def simple_form(request, form, message='Guardado correctamente'):
    if request.POST:
        form = form(request.POST)
        if form.is_valid():
            form.save(request)
        messages.success(request, f'{message}')            
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def save_default_currency(request):
    return simple_form(request, DefaultCurrencyForm, 
        message='Guardado correctamente')
        

@login_required(login_url='login')
def save_cashflow_movement(request):
    return simple_form(request, CashflowMoveForm, 
        message='Guardado correctamente')


@login_required(login_url='login')
def save_asset_movement(request):
    return simple_form(request, PositionMovementForm, 
        message='Guardado correctamente')


@login_required(login_url='login')
def save_new_asset_movement(request):
    if request.POST:
        form = AddNewAssetForm(request.POST)
        if form.is_valid():
            empresa_ticker = request.POST['stock'].split(' (')[1]
            ticker = empresa_ticker[:-1]
            empresa_busqueda = Company.objects.get(ticker = ticker)
            form.save(request, empresa_busqueda)
        messages.success(request, f'Guardado correctamente')            
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def save_new_category(request):
    return simple_form(request, AddCategoriesForm, 
        message='Guardado correctamente')


@login_required(login_url='login')
def save_new_objectif(request):
    return simple_form(request, FinancialObjectifForm, 
        message='Guardado correctamente')


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