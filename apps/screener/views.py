from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.empresas.models import Company, ExchangeOrganisation
from apps.etfs.models import Etf
from apps.empresas.company.update import UpdateCompany
from apps.empresas.valuations import discounted_cashflow


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
    paginate_by = 50

    def get_queryset(self, **kwargs):
       return Company.objects.clean_companies_by_main_exchange(self.kwargs['name'])

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
        return get_object_or_404(
            Company.objects.prefetch_related(
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
            ),
            ticker=ticker)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empresa = self.object
        UpdateCompany(empresa).general_update()
        self.request.session['screener'] = empresa.id
        context["meta_desc"] = f'Estudia a fondo la empresa {empresa.name}. Más de 30 años de información, noticias, pros, contras y mucho más'
        context["meta_tags"] = f'finanzas, blog financiero, blog el financiera, invertir, {empresa.name}, {empresa.ticker}'
        context["meta_title"] = f'Análisis completo de {empresa.name}'
        context["meta_url"] = f'/screener/analisis-de/{empresa.ticker}/'
        context['company_is_fav'] = False
        if self.request.user.is_authenticated and empresa.ticker in self.request.user.fav_stocks.only('ticker'):
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
