from django.shortcuts import render
from django.conf import settings
from django.views.generic import (
	ListView,
	DetailView,
	CreateView)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
		queryset = Term.objects.filter(status = 1)
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


class TermCorrectionView(SuccessMessageMixin, CreateView):
	form_class = CreateCorrectionForm
	template_name = 'glosario/correction.html'
	success_message = 'Gracias por tu aporte'

	def get_object(self):
		return TermContent.objects.get(id = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['public_key'] = settings.GOOGLE_RECAPTCHA_PUBLIC_KEY
		context['object'] = self.get_object()
		return context

	def get_initial(self, *args, **kwargs):
		initial = super(TermCorrectionView, self).get_initial(**kwargs)
		object = self.get_object()
		initial['title'] = object.title
		initial['content'] = object.content
		initial['term_content_related'] = object
		return initial
	
	def post(self, request, *args: str, **kwargs):
		form = self.get_form(self.get_form_class())
        
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
				email = self.request.POST.get('email')
				user = User.objects.get_or_create_quick_user(email, self.request, just_correction = True)
			else:
				messages.error(self.request, 'Hay un error con el captcha')
				return self.form_invalid(form)
		else:
			user = self.request.user

		return self.form_valid(form, user)

	def form_valid(self, form, user):
		form.instance.reviwed_by = user
		return super().form_valid(form)

