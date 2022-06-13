from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages

from apps.empresas.models import (
    Company, 
    ExchangeOrganisation
)
from apps.etfs.models import Etf
from apps.empresas.company.update import UpdateCompany
from apps.seo.views import SEOListView, SEODetailView

from .models import YahooScreener

class ScreenerInicioView(SEOListView):
    model = ExchangeOrganisation
    context_object_name = "organisations"
    template_name = 'screener/inicio.html'
    meta_description = 'Estudia todos loas activos que quieras para ser el mejor inversor. Ten acceso a más de 30000 empresas y 30 años de información.'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'
    meta_title = 'Más de 30 años de información financiera de cualquier activo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["screeners"] = YahooScreener.objects.all()
        return context


class CompanyScreenerInicioView(SEOListView):
    model = Company
    template_name = 'screener/empresas/inicio.html'
    context_object_name = "empresas"
    paginate_by = 50
    slug_url_kwarg = 'slug'
    meta_description = 'Estudia todas las empresas que quieras para ser el mejor inversor. Ten acceso a más de 30000 empresas y 30 años de información.'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'
    # meta_title = 

    def get_queryset(self, **kwargs):
       return Company.objects.clean_companies_by_main_exchange(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.kwargs['slug']
        context["meta_title"] = f'Más de 30 años de información financiera de cualquier empresa de {name}'
        context["meta_url"] = f'/screener/empresas-de/{name}/'
        return context


class AllYahooScreenersView(SEOListView):
    model = YahooScreener
    template_name = 'screener/yahoo-screeners/all-screeners.html'
    context_object_name = "screeners"
    meta_title = "Los mejores screeners"


class YahooScreenerView(SEODetailView):
    model = YahooScreener
    template_name = 'screener/yahoo-screeners/screener.html'
    context_object_name = "screener"
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    meta_tags = 'empresas, inversiones, analisis de empresas, invertir'


class EtfScreenerInicioView(ListView):
    model = Etf
    template_name = 'screener/etfs/inicio.html'
    context_object_name = "etfs"


class CompanyDetailsView(SEODetailView):
    model = Company
    template_name = 'screener/empresas/details.html'
    context_object_name = "the_company"
    slug_field = 'ticker'

    def get_object(self):
        ticker = self.kwargs.get('ticker')
        try:
            response = Company.objects.prefetch_related(
                'inc_statements',
                'balance_sheets',
                'cf_statements',
                'rentability_ratios',
                'liquidity_ratios',
                'margins',
                'fcf_ratios',
                'per_share_values',
                'non_gaap_figures',
                'operation_risks_ratios',
                'ev_ratios',
                'growth_rates',
                'efficiency_ratios',
                'price_to_ratios'
            ).only(
                'ticker',
                'name',
                'sector',
                'website',
                'state',
                'country',
                'ceo',
                'image',
                'city',
                'employees',
                'address',
                'zip_code',
                'cik',
                'cusip',
                'isin',
                'description',
                'ipoDate',
            ).get(ticker=ticker)
        # except model.DoesNotExist:
        except Exception as e:
            response, _ = Company.objects.get_or_create(
                name='Need-parsing',
                ticker=ticker
            )            
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = self.object
        UpdateCompany(empresa).general_update()
        self.request.session['screener'] = empresa.id
        context["meta_desc"] = f'Estudia a fondo la empresa {empresa.name}. Más de 30 años de información, noticias, análisis FODA y mucho más'
        context["meta_tags"] = f'finanzas, blog financiero, blog el financiera, invertir, {empresa.name}, {empresa.ticker}'
        context["meta_title"] = f'Análisis completo de {empresa.name}'
        company_is_fav = False
        limit_years = 10
        has_bought = False
        if self.request.user.is_authenticated:
            if empresa.ticker in self.request.user.fav_stocks.only('ticker'):
                company_is_fav = True
        
        context['has_bought'] = has_bought
        context['company_is_fav'] = company_is_fav
        context['complete_info'] = empresa.complete_info(limit_years)
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.name == 'Need-parsing':
            messages.error(self.request, 'Lo sentimos, esta empresa todavía no tiene información ahora mismo vamos a recabar información y estará lista en poco tiempo')
            return redirect(reverse('screener:screener_inicio'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class EtfDetailsView(DetailView):
    model = Etf
    template_name = 'screener/etfs/details.html'
    context_object_name = "etf"
    slug_field = 'ticker'

    def get_object(self):
        ticker = self.kwargs.get('ticker')
        return get_object_or_404(Etf, ticker=ticker)
