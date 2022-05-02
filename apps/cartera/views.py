from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import (
	TemplateView,
	DetailView,
	CreateView)
from django.http.response import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from apps.general.models import Currency

from .models import (
	Patrimonio
)
from .forms import (
    CashflowMoveForm,
    DefaultCurrencyForm,
    AddCategoriesForm,
    FinancialObjectifForm
)

User = get_user_model()


class InicioCarteraView(LoginRequiredMixin, TemplateView):
    template_name = "cartera/private/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patrimonio"] = Patrimonio.objects.get_or_create(user = self.request.user)[0]
        context["cashflowform"] = CashflowMoveForm()
        context["defcurrencyform"] = DefaultCurrencyForm()

        context["asset_movement_form"] = DefaultCurrencyForm()
        context["new_asset_form"] = DefaultCurrencyForm()
        
        context["add_categories_form"] = AddCategoriesForm()
        context["add_financial_objective_form"] = FinancialObjectifForm()
        context["meta_title"] = 'Tu gestor patrimonial'
        return context


@login_required(login_url='login')
def save_default_currency(request):
    if request.POST:
        form = CashflowMoveForm(request.POST)
        if form.is_valid():
            form.save_currency(request.user)
        messages.success(request, f'Guardado correctamente')            
        return redirect(request.META.get('HTTP_REFERER'))
        

@login_required(login_url='login')
def save_cashflow_movement(request):
    if request.POST:
        form = CashflowMoveForm(request.POST)
        if form.is_valid():
            form.create_cashflow(request.user)
        messages.success(request, f'Guardado correctamente')
        return redirect(request.META.get('HTTP_REFERER')) 


@login_required(login_url='login')
def save_asset_movement(request):
    if request.POST:
        form = CashflowMoveForm(request.POST)
        if form.is_valid():
            form.create_cashflow(request.user)
        messages.success(request, f'Guardado correctamente')
        return redirect(request.META.get('HTTP_REFERER')) 


@login_required(login_url='login')
def save_new_asset_movement(request):
    if request.POST:
        form = CashflowMoveForm(request.POST)
        if form.is_valid():
            form.create_cashflow(request.user)
        messages.success(request, f'Guardado correctamente')
        return redirect(request.META.get('HTTP_REFERER')) 


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