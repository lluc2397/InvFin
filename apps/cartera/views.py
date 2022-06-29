from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
	Patrimonio
)
User = get_user_model()


class DefaultCateraView(LoginRequiredMixin, TemplateView):
    meta_title = None        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        patrimoine = Patrimonio.objects.get_or_create(user=user)[0]
        context["patrimonio"] = patrimoine
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
    user = request.user
    overall_portfolio_information = user.user_patrimoine.overall_portfolio_information
    return render(request, 'cartera/tables/balance.html', {'overall_portfolio_information': overall_portfolio_information})