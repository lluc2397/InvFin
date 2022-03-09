from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q

from apps.empresas.models import Company, ExchangeOrganisation, Exchange
from apps.etfs.models import Etf

from .models import (
    UserCompanyObservation,
    FavoritesStocksHistorial,
    FavoritesStocksList,
    UserScreenerMediumPrediction,
    UserScreenerSimplePrediction)

from .forms import UserCompanyObservationForm


from apps.empresas.utils import UpdateCompany
import json


class ScreenerInicioView(ListView):
    model = ExchangeOrganisation
    context_object_name = "organisations"
    template_name = 'screener/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta_desc"] = 'Estudia todos loas activos que quieras para ser el mejor inversor. Ten acceso a más de 30000 empresas y 30 años de información.'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = 'Más de 30 años de información financiera de cualquier activo'
        context["meta_url"] = '/screener/'
        return context


class CompanyScreenerInicioView(ListView):
    model = Company
    template_name = 'screener/empresas/inicio.html'
    context_object_name = "empresas"

    def get_queryset(self, **kwargs):
       query = super().get_queryset(**kwargs)
       the_org = ExchangeOrganisation.objects.get(name = self.kwargs['name'])
       return query.filter(exchange__in = [exch for exch in Exchange.objects.filter(main_org = the_org)],
        no_incs = False,
        no_bs = False,
        no_cfs = False,)[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs['name']
        context["meta_desc"] = 'Estudia todas las empresas que quieras para ser el mejor inversor. Ten acceso a más de 30000 empresas y 30 años de información.'
        context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
        context["meta_title"] = f'Más de 30 años de información financiera de cualquier empresa de {name}'
        context["meta_url"] = f'/screener/empresas-de/{name}/'
        return context


class EtfScreenerInicioView(ListView):
    model = Etf
    template_name = 'screener/etfs/inicio.html'
    context_object_name = "etfs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[''] = ''
        return context


class CompanyDetailsView(DetailView):
    model = Company
    template_name = 'screener/empresas/details.html'
    context_object_name = "the_company"
    slug_field = 'ticker'

    def get_object(self):
        ticker = self.kwargs.get('ticker')
        return get_object_or_404(Company, ticker=ticker)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = self.get_object()
        UpdateCompany(empresa).general_update()
        context["meta_desc"] = f'Estudia a fondo la empresa {empresa.name}. Más de 30 años de información, noticias, pros, contras y mucho más'
        context["meta_tags"] = f'finanzas, blog financiero, blog el financiera, invertir, {empresa.name}, {empresa.ticker}'
        context["meta_title"] = f'Análisis completo de {empresa.name}'
        context["meta_url"] = f'/screener/analisis-de/{empresa.ticker}/'

        context['observation_form'] = UserCompanyObservationForm()
        context['company_is_fav'] = False
        if self.request.user.is_authenticated and empresa in self.request.user.fav_stocks:
            context['company_is_fav'] = True
        return context


class EtfDetailsView(DetailView):
    model = Etf
    template_name = 'screener/etfs/details.html'
    context_object_name = "etf"
    slug_field = 'ticker'

    def get_object(self):
        ticker = self.kwargs.get('ticker')
        return get_object_or_404(Etf, ticker=ticker)


class CreateCompanyObservationView(CreateView):
    model = UserCompanyObservation
    fields = ['observation', 'observation_type']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = self.request.POST['company']
        form.save()	
        return super(CreateCompanyObservationView, self).form_valid(form)


def suggest_list_search_companies(request):
	if request.is_ajax():
		query = request.GET.get("term", "")
		companies_availables = Company.objects.filter(Q(name__icontains=query) | Q(ticker__icontains=query),
		no_incs = False,
		no_bs = False,
		no_cfs = False,
			)[:10]
		
		results = []
		for company in companies_availables:
			result = f'{company.name} ({company.ticker})'
			results.append(result)

		data = json.dumps(results)
	mimetype = "application/json"
	return HttpResponse(data, mimetype)