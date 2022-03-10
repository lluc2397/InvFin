from django.shortcuts import render
from django.views.generic import (
	ListView,
	DetailView,
	CreateView)
from django.contrib.messages.views import SuccessMessageMixin

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
		model = self.get_object()
		model.total_views += 1
		model.save()
		return context


class TermCorrectionView(SuccessMessageMixin, CreateView):
	model = TermContent
	form_class = CreateCorrectionForm
	template_name = 'glosario/correction.html'
	success_message = 'Gracias por tu aporte'
	slug_field = 'pk'

	def get_initial(self, *args, **kwargs):
		initial = super(TermCorrectionView, self).get_initial(**kwargs)
		initial['title'] = self.get_object().title
		initial['content'] = self.get_object().content
		return initial

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

