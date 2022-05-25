from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS
from rest_framework import status

from apps.empresas.company.retreive_data import RetreiveCompanyData
from apps.empresas.valuations import discounted_cashflow
from apps.empresas.models import Company

from ..models import (
    UserCompanyObservation,
    UserScreenerMediumPrediction,
    UserScreenerSimplePrediction,
    YahooScreener
)
from ..forms import UserCompanyObservationForm

import json
import yahooquery as yq


User = get_user_model()


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class CompanyBaseAPIView(APIView):
    serializer_class = None
    permission_classes = [AllowAny|ReadOnly]

    def get(self, request):
        model = self.serializer_class.Meta.model
        queryset = model.objects.filter(company__ticker = request.GET['ticker'])[:10]
        serializer = self.serializer_class(queryset, many=True)
        if status.is_success:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class CompanyFODAListView(ListView):
    model = UserCompanyObservation
    template_name = 'screener/empresas/company_parts/foda/foda_parts.html'
    context_object_name = "foda_analysis"

    def get_queryset(self):
        return UserCompanyObservation.objects.filter(company__id = self.kwargs['id'])


def get_company_price(request, ticker):
    prices = RetreiveCompanyData(ticker).get_current_price()
    return render(request, 'screener/headers/company_price.html', {
        'prices': prices,
    })


def get_company_news(request, ticker):
    news = RetreiveCompanyData(ticker).get_news()
    return render(request, 'screener/empresas/company_parts/resume/news.html', {
        'show_news': news,
    })


def get_company_valuation(request, ticker):
    company_valuation = Company.objects.get(ticker=ticker).calculate_current_ratios()
    return render(request, 'screener/empresas/company_parts/valuations/response.html', {
        'company_valuation': company_valuation,
    })


def retreive_yahoo_screener_info(request, query):
    yahoo = yq.Screener().get_screeners(query)
    context = {
        'yahoo': yahoo[query]['quotes']
    }
    return render(request, 'screener/yahoo-screeners/screener-data.html', context)


def retreive_top_lists(request):
    yahoo = yq.Screener().get_screeners(['most_actives', 'day_gainers', 'day_losers'], 5)
    extra = {
        'positive': 'text-success',
        'negative': 'text-danger'
    }
    url = '/screener/analisis-de/'
    day_gainers = {
        'title': 'Mayor aumento de precio',
        'subtitle': 'day_gainers',
        'slug': YahooScreener.objects.get(yq_name='day_gainers').slug,
        'extra': extra,
        'url': url,
        'data': yahoo['day_gainers']['quotes']
    }
    day_losers = {
        'title': 'Mayor disminución de precio',
        'subtitle': 'day_losers',
        'slug': YahooScreener.objects.get(yq_name='day_losers').slug,
        'extra': extra,
        'url': url,
        'data': yahoo['day_losers']['quotes']
    }
    most_actives = {
        'title': 'Más activos',
        'subtitle': 'most_actives',
        'slug': YahooScreener.objects.get(yq_name='most_actives').slug,
        'extra': extra,
        'url': url,
        'data': yahoo['most_actives']['quotes']
    }

    gainers_actives_losers = [
        day_gainers,
        most_actives,
        day_losers
    ]
    return render(request, 'screener/yahoo-screeners/top-lists.html', {
        'gainers_actives_losers': gainers_actives_losers,
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