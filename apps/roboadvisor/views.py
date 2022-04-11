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
    template_name = "TEMPLATE_NAME"
