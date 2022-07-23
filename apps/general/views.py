import base64
import json

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import ListView, TemplateView

from apps.empresas.models import Company
from apps.escritos.models import FavoritesTermsHistorial, FavoritesTermsList, Term
from apps.screener.models import FavoritesStocksHistorial
from apps.super_investors.models import (
    FavoritesSuperinvestorsHistorial,
    FavoritesSuperinvestorsList,
    Superinvestor,
)

from .models import Notification


class MessagesTemplateview(TemplateView):
	template_name = "complements/messages.html"


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
			result = f'Empresa: {company.name} [{company.ticker}]'
			results.append(result)
		
		for term in terms_availables:
			result = f'Término: {term.title}'			
			results.append(result)

		data = json.dumps(results)
		mimetype = "application/json"
		return HttpResponse(data, mimetype)


def search_results(request):
	if request.POST:
		term = request.POST['term']
		query = term[:7]
		if query == 'Empresa':
			empresa_ticker = term.split(' [')[1]
			ticker = empresa_ticker[:-1]
			empresa_busqueda = Company.objects.get(ticker = ticker)
			redirect_to = empresa_busqueda.get_absolute_url()
		
		elif query == 'Término':
			title = term.split(':')[1]
			title = title[1:]
			try:
				term_busqueda = Term.objects.get(title = title)
			except Term.MultipleObjectsReturned:
				term_busqueda = Term.objects.filter(title = title).first()
			redirect_to = term_busqueda.get_absolute_url()
		
		else:
			if term.isupper():
				empresa_busqueda = Company.objects.filter(ticker = term)
				if empresa_busqueda.exists():
					redirect_to = empresa_busqueda[0].get_absolute_url()
			elif term.isupper() == False:
				empresa_busqueda = Company.objects.filter(name__icontains = term)
				if empresa_busqueda.exists():
					redirect_to = empresa_busqueda[0].get_absolute_url()
			else:
				messages.warning(request, 'No hemos entendido tu búsqueda')
				return redirect(request.META.get('HTTP_REFERER'))
				
		return redirect(redirect_to)
	else:
		return redirect(request.META.get('HTTP_REFERER'))


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
		
		elif 'term' in data.keys():
			term_id = data.get('term')
			current_term = Term.objects.get(id = term_id)
			try:
				user.favorites_terms
			except:
				FavoritesTermsList.objects.create(user = user)
			if current_term in user.fav_terms:
				user.favorites_terms.term.remove(current_term)
				FavoritesTermsHistorial.objects.create(user = user, term = current_term, removed = True)
				is_favorite = False
			else:
				FavoritesTermsHistorial.objects.create(user = user, term = current_term, added = True)
				user.favorites_terms.term.add(current_term)
				is_favorite = True
		
		elif 'investor' in data.keys():
			superinvestor = data.get('investor')
			current_superinvestor = Superinvestor.objects.get(slug = superinvestor)
			try:
				user.favorites_superinvestors
			except:
				FavoritesSuperinvestorsList.objects.create(user=user)
			if current_superinvestor in user.fav_superinvestors:
				user.favorites_superinvestors.superinvestor.remove(current_superinvestor)
				FavoritesSuperinvestorsHistorial.objects.create(user=user, superinvestor=current_superinvestor, removed=True)
				is_favorite = False
			else:
				FavoritesSuperinvestorsHistorial.objects.create(user=user, superinvestor=current_superinvestor, added=True)
				user.favorites_superinvestors.superinvestor.add(current_superinvestor)
				is_favorite = True
				
		return JsonResponse ({'is_favorite':is_favorite})


def coming_soon(request):
	return render(request, 'complements/coming_soon.html')


def email_opened_view(request, uidb64):
    
    pixel_gif = base64.b64decode(b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=')
    
    if request.method == 'GET':
        decoded_url = force_text(urlsafe_base64_decode(uidb64)).split("-")
        id, app_label, object_name = decoded_url[0], decoded_url[1], decoded_url[2]
        modelo = apps.get_model(app_label, object_name, require_ready=True).objects.get(id=id)
        modelo.opened = True
        modelo.date_opened = timezone.now()
        modelo.save()
        return HttpResponse(pixel_gif, content_type='image/gif')  


class NotificationsListView(LoginRequiredMixin, ListView):
	model = Notification
	template_name = 'notifications/notifications_page.html'

	def get_queryset(self):
		notifications = Notification.objects.filter(user = self.request.user)
		notifications.update(is_seen = True)
		return notifications


@login_required(login_url='login')
def delete_notification(request, notif_id):
    user = request.user
    Notification.objects.get(id = notif_id, user = user).delete()
    return redirect("general:notifications_list")