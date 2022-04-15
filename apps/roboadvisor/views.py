from django.shortcuts import render
from django.views.generic import (
	ListView,
	View,
	DetailView,
	CreateView,
	UpdateView)


from .models import (
    RoboAdvisorService
)


#For the differents questions it could be easier to create a template for each form
#when a service is requested, all the templates are hidden with css
#when a form is submited we hide the previous question and we show the next one
#the forms should be saved each time?


class RoboAdvisorServicesListView(ListView):
	model = RoboAdvisorService
	template_name = "roboadvisor/inicio.html"
	context_object_name = "services"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["meta_desc"] = 'IA para mejorar las inversiones'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir, roboadvisor'
		context["meta_title"] = 'Tu consejero inteligente'
		context["meta_url"] = '/roboadvisor/'
		return context


class RoboAdvisorServiceOptionView(DetailView):
	model = RoboAdvisorService
	template_name = "roboadvisor/details.html"

