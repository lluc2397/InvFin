from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

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


class DefaultCateraView(LoginRequiredMixin, TemplateView):
    meta_title = None        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        patrimoine = Patrimonio.objects.get_or_create(user=user)[0]
        context["patrimonio"] = patrimoine
        initial = {'currency': patrimoine.default_currency}
            
        context["cashflowform"] = CashflowMoveForm(initial=initial)
        context["defcurrencyform"] = DefaultCurrencyForm(initial=initial)

        context["asset_movement_form"] = PositionMovementForm(user=user, initial=initial)
        context["new_asset_form"] = AddNewAssetForm(initial=initial)

        context["add_categories_form"] = AddCategoriesForm()
        context["add_financial_objective_form"] = FinancialObjectifForm()
        context["meta_title"] = self.meta_title
        return context


class InicioCarteraView(DefaultCateraView):
    template_name = "cartera/private/inicio.html"
    meta_title = 'Tu gestor patrimonial'


class InicioPortfolioView(DefaultCateraView):
    template_name = "cartera/private/cartera.html"
    meta_title = 'Tu cartera'


class InicioCashflowView(DefaultCateraView):
    template_name = "cartera/private/financials.html"
    meta_title = 'Tus finanzas'


def return_balance_table(request):
    return render(request, 'cartera/tables/balance.html', {})