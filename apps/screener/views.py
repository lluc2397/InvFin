from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q

from apps.empresas.models import Company, ExchangeOrganisation
from apps.etfs.models import Etf
from apps.empresas.company.update import UpdateCompany
from apps.empresas.company.extension import get_news
from apps.empresas.valuations import discounted_cashflow

from .models import (
    UserCompanyObservation,
    UserScreenerMediumPrediction,
    UserScreenerSimplePrediction
)
from .forms import UserCompanyObservationForm

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
    paginate_by = 50

    def get_queryset(self, **kwargs):
       query = super().get_queryset(**kwargs)
       return query.filter(exchange__main_org__name = self.kwargs['name'],
            no_incs = False,
            no_bs = False,
            no_cfs = False)

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


class CompanyFODAListView(ListView):
    model = UserCompanyObservation
    template_name = 'screener/empresas/company_parts/foda/foda_parts.html'
    context_object_name = "foda_analysis"

    def get_queryset(self):
        return UserCompanyObservation.objects.filter(company__id = self.kwargs['id'])


def return_company_news(request, ticker):
    news = get_news(ticker)
    return render(request, 'screener/empresas/company_parts/resume/news.html', {
        'show_news': news,
    })


def create_company_observation(request):
    if request.method == 'POST':
        company_id = request.session['screener']
        form = UserCompanyObservationForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.user = request.user
            company = Company.objects.get(id = company_id)
            model.company = company
            model.save(update_fields=['user', 'company'])
            return HttpResponse(status=204, headers={'HX-Trigger': 'refreshObservationsCompany'})
        else:
            print(form.errors)
            return HttpResponse(status=500)
    else:
        form = UserCompanyObservationForm()
    return render(request, 'screener/empresas/company_parts/foda/foda_modal.html', {
        'form': form,
    })


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


def medium_valuation_view(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            
            opt_growth = float(data.get('complex_opt_growth').replace(',', '.'))
            neu_growth = float(data.get('complex_neu_growth').replace(',', '.'))
            pes_growth = float(data.get('complex_pes_growth').replace(',', '.'))
            company_id = data.get('company_id')
            current_per = float(data.get('current_per').replace(',', '.'))
            opt_margin = float(data.get('complex_opt_margin').replace(',', '.'))
            neu_margin = float(data.get('complex_neu_margin').replace(',', '.'))
            pes_margin = float(data.get('complex_pes_margin').replace(',', '.'))
            opt_buyback = float(data.get('complex_opt_buyback').replace(',', '.'))
            neu_buyback = float(data.get('complex_neu_buyback').replace(',', '.'))
            pes_buyback = float(data.get('complex_pes_buyback').replace(',', '.'))
            opt_fcf_margin = float(data.get('complex_opt_fcf_margin').replace(',', '.'))
            neu_fcf_margin = float(data.get('complex_neu_fcf_margin').replace(',', '.'))
            pes_fcf_margin = float(data.get('complex_pes_fcf_margin').replace(',', '.'))

            the_company = Company.objects.get(id = company_id)
            last_revenue = the_company.most_recent_inc_statement.revenue
            average_shares_out = the_company.most_recent_inc_statement.weighted_average_shares_outstanding

            UserScreenerMediumPrediction.objects.create(
                user = user, 
                company = the_company,
                optimistic_growth = opt_growth,
                neutral_growth = neu_growth,
                pesimistic_growth = pes_growth,
                optimistic_margin = opt_margin,
                neutral_margin = neu_margin,
                pesimistic_margin = pes_margin,
                optimistic_buyback = opt_buyback,
                neutral_buyback = neu_buyback,
                pesimistic_buyback = pes_buyback,
                optimistic_fcf_margin = opt_fcf_margin,
                neutral_fcf_margin = neu_fcf_margin,
                pesimistic_fcf_margin = pes_fcf_margin,
                )

            opt_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = opt_growth,
                net_income_margin = opt_margin,
                fcf_margin = opt_fcf_margin,
                buyback = opt_buyback,
                average_shares_out = average_shares_out
            )
            neu_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = neu_growth,
                net_income_margin = neu_margin,
                fcf_margin = opt_fcf_margin,
                buyback = neu_buyback,
                average_shares_out = average_shares_out
                )
            pes_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = pes_growth,
                net_income_margin = pes_margin,
                fcf_margin = opt_fcf_margin,
                buyback = pes_buyback,
                average_shares_out = average_shares_out
                )

            return JsonResponse ({'complex_opt_valuation':opt_valuation, 
            'complex_neu_valuation':neu_valuation, 'complex_pes_valuation':pes_valuation
            })



def simple_valuation_view(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            

            opt_growth = float(data.get('opt_grow').replace(',', '.'))
            neu_growth = float(data.get('neu_grow').replace(',', '.'))
            pes_growth = float(data.get('pes_grow').replace(',', '.'))
            company_id = data.get('comp')
            buyback = float(data.get('buyback').replace(',', '.'))
            
            the_company = Company.objects.get(id = company_id)
            last_revenue = the_company.most_recent_inc_statement.revenue
            average_shares_out = the_company.most_recent_inc_statement.weighted_average_shares_outstanding
            net_income_margin = the_company.most_recent_margins.net_income_margin
            fcf_margin = the_company.most_recent_margins.fcf_margin
            buyback = buyback

            UserScreenerSimplePrediction.objects.create(
                user = user,
                company = the_company,
                optimistic_growth = opt_growth,
                neutral_growth = neu_growth,
                pesimistic_growth = pes_growth
                
                )

            opt_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = opt_growth,
                net_income_margin = net_income_margin,
                fcf_margin = fcf_margin,
                buyback = buyback,
                average_shares_out = average_shares_out
            )
            neu_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = neu_growth,
                net_income_margin = net_income_margin,
                fcf_margin = fcf_margin,
                buyback = buyback,
                average_shares_out = average_shares_out
                )
            pes_valuation = discounted_cashflow(
                last_revenue = last_revenue,
                revenue_growth = pes_growth,
                net_income_margin = net_income_margin,
                fcf_margin = fcf_margin,
                buyback = buyback,
                average_shares_out = average_shares_out
                )

            return JsonResponse ({'opt_valuation':opt_valuation, 
            'neu_valuation':neu_valuation, 'pes_valuation':pes_valuation
            })