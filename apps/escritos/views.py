from django.shortcuts import redirect, render
from django.conf import settings
from django.views.generic import (
	ListView,
	DetailView,
	CreateView)
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


import json
import urllib

from .models import (
    Term,
    TermContent,
    TermCorrection
)

from .forms import CreateCorrectionForm

class GlosarioView(ListView):
	model = Term
	template_name = 'glosario/inicio.html'
	ordering = ['title']
	context_object_name = "terms"
	paginate_by = 10

	def get_queryset(self):
		queryset = Term.objects.clean_terms()
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["meta_desc"] = 'Todos los términos y definiciones que encesitas conocer'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir'
		context["meta_title"] = 'El diccionario que necesitas como inversor'
		context["meta_url"] = '/diccionario-financiero/'
		return context


class TermDetailsView(DetailView):
	model = Term
	template_name = 'glosario/details.html'
	context_object_name = "object"
	slug_field = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		model = self.object
		model.total_views += 1
		model.save()
		return context


# class CreateTermCorrectionView(SuccessMessageMixin, CreateView):


class TermCorrectionView(CreateView):
	form_class = CreateCorrectionForm
	template_name = 'glosario/correction.html'
	success_message = 'Gracias por tu aporte'

	def get_object(self):
		return TermContent.objects.get(id = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['public_key'] = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
		object = self.get_object()
		context['object'] = object
		initial = {
			'title': object.title,
			'content': object.content,
			'term_content_related': object
		}
		context['form'] = CreateCorrectionForm(initial)
		return context

	def post(self, request, *args, **kwargs):
		form = CreateCorrectionForm(request.POST)
        
		if self.request.user.is_anonymous:
			recaptcha_response = self.request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
				'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response': recaptcha_response
			}
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())

			if result['success']:
				email = request.POST.get('email')
				user = User.objects.get_or_create_quick_user(email, self.request, just_correction = True)
			else:
				messages.error(self.request, 'Hay un error con el captcha')
				return self.form_invalid(form)
		else:
			user = self.request.user
		
		if form.is_valid():
			return self.form_valid(form, user)
		return self.form_invalid(form)
	
	def form_valid(self, form, user):
		form.instance.reviwed_by = user
		model = form.save()
		messages.success(self.request, self.success_message)
		return redirect(model.get_absolute_url())

