from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.apps import apps
from django.views.generic import TemplateView, RedirectView
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q
from django.urls import reverse

import json

from apps.escritos.models import Term, FavoritesTermsHistorial
from apps.public_blog.models import PublicBlog
from apps.empresas.models import Company
from apps.screener.models import FavoritesStocksHistorial

@login_required
def create_comment_view(request, url_encoded):
	if request.method == 'POST':
		user = request.user
		if user.is_authenticated:
			content = request.POST.get('comment_content')
			decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
			id, app_label, object_name = decoded_url[0], decoded_url[1], decoded_url[2]
			modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
			modelo.comments_related.create(author = user, content=content, content_related = modelo)
			messages.success(request, 'Comentario agregado')
		return redirect (modelo.get_absolute_url())


@login_required
def create_vote_view(request, url_encoded):
	if request.method == 'POST':
		user = request.user
		if user.is_authenticated:
			decoded_url = force_text(urlsafe_base64_decode(url_encoded)).split("-")
			id, app_label, object_name, vote = decoded_url[0], decoded_url[1], decoded_url[2], decoded_url[3]
			modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
			if modelo.author == user:
				messages.error(request, 'No puedes votarte a ti mismo')
				return redirect (modelo.get_absolute_url())
			vote_result = modelo.vote(user, vote)
			if vote_result == 0:
				messages.error(request, 'Ya has votado')
				return redirect (modelo.get_absolute_url())
			messages.success(request, 'Voto aportado')
		return redirect (modelo.get_absolute_url())
		

def suggest_list_search(request):
	if request.is_ajax():
		query = request.GET.get("term", "")
		companies_availables = Company.objects.filter(Q(name__icontains=query) | Q(ticker__icontains=query),
		no_incs = False,
		no_bs = False,
		no_cfs = False,
			)[:4]
		
		# terms_availables = Term.objects.filter(Q(title__icontains=query), status = 1)[:3]
		terms_availables = Term.objects.filter(Q(title__icontains=query))[:4]
		
		results = []
		for company in companies_availables:
			result = f'empresa: {company.name} ({company.ticker})'
			results.append(result)
		
		for term in terms_availables:
			result = f'termino: {term.title}'			
			results.append(result)

		data = json.dumps(results)
		mimetype = "application/json"
		return HttpResponse(data, mimetype)


def search_results(request):
	if request.POST:
		term = request.POST['term']
		query = term.split(':')[0]
		if query == 'empresa':
			empresa_ticker = term.split(' (')[1]
			ticker = empresa_ticker[:-1]
			empresa_busqueda = Company.objects.get(ticker = ticker)
			redirect_to = empresa_busqueda.get_absolute_url()
		else:
			title = term.split(':')[1]
			title = title[1:]
			term_busqueda = Term.objects.get(title = title)
			redirect_to = term_busqueda.get_absolute_url()

	return redirect(redirect_to)


@login_required
def update_favorites(request):
	user = request.user
    
	if request.method == 'POST':
		data = json.load(request)

		if 'ticker' in data.keys():
			ticker = data.get('ticker')
			current_stock = Company.objects.get(ticker = ticker)

			if current_stock in user.fav_stocks:
				user.favorites_companies.stock.remove(current_stock)
				FavoritesStocksHistorial.objects.create(user = user, asset = current_stock, removed = True)
				is_favorite = False
			else:
				FavoritesStocksHistorial.objects.create(user = user, asset = current_stock, added = True)
				user.favorites_companies.stock.add(current_stock)
				is_favorite = True
		
		else:
			term_id = data.get('term')
			current_term = Term.objects.get(id = term_id)

			if current_term in user.fav_stocks:
				user.favorites_terms.term.remove(current_term)
				FavoritesTermsHistorial.objects.create(user = user, term = current_term, removed = True)
				is_favorite = False
			else:
				FavoritesTermsHistorial.objects.create(user = user, term = current_term, added = True)
				user.favorites_terms.term.add(current_term)
				is_favorite = True
				
		return JsonResponse ({'is_favorite':is_favorite})


class EscritosView(TemplateView):
    template_name = 'escritos/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['terms'] = Term.objects.filter(status = 1)
        context['blogs'] = PublicBlog.objects.filter(status = 1)
        return context
