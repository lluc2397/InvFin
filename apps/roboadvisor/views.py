from django.views.generic import ListView, DetailView

from .mixins import ServicePaymentMixin
from .models import (
    RoboAdvisorService,
	RoboAdvisorUserServiceActivity
)
from .forms import (
	RoboAdvisorQuestionInvestorExperienceForm,
	RoboAdvisorQuestionCompanyAnalysisForm,
	RoboAdvisorQuestionFinancialSituationForm,
	RoboAdvisorQuestionPortfolioAssetsWeightForm,
	RoboAdvisorQuestionPortfolioCompositionForm,
	RoboAdvisorQuestionRiskAversionForm
)
from .brain.investor import get_investor_type
# If user ask for a company recom and it doesn't have profile, recommend to tkae the test

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

		if 'roborequest' in self.request.GET:
			# Show banner to help starting to get credits and start roboadvisor
			context["no_profile"] = ''
		return context


class RoboAdvisorServiceOptionView(DetailView):
	model = RoboAdvisorService
	template_name = "roboadvisor/details.html"
	context_object_name = "service"

	def prepare_forms(self, user, service):
		context_forms = {}
		if RoboAdvisorUserServiceActivity.objects.filter(user = user, service = service, status = 2).exists():
			# get pre filed data
			pass
		
		context_forms["experience_form"] = RoboAdvisorQuestionInvestorExperienceForm()
		context_forms["company_analysis_form"] = RoboAdvisorQuestionCompanyAnalysisForm()
		context_forms["financial_situation_form"] = RoboAdvisorQuestionFinancialSituationForm()
		context_forms["risk_aversion_form"] = RoboAdvisorQuestionRiskAversionForm()
		context_forms["assets_weight_form"] = RoboAdvisorQuestionPortfolioAssetsWeightForm()
		context_forms["portfolio_asset_form"] = RoboAdvisorQuestionPortfolioCompositionForm()

		return context_forms


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		service = self.get_object()
		user = self.request.user

		context["meta_title"] = f'{service.title}'
		context["meta_url"] = f'/robo-option/{service.slug}/'

		context.update(self.prepare_forms(user, service))		

		default_data = {
			'user': user,
			'service': service
		}

		service_activity = RoboAdvisorUserServiceActivity.objects.create(**default_data)
		self.request.session['service_activity'] = service_activity.id
		context['service_activity'] = service_activity.id

		return context
       

class RoboAdvisorResultView(DetailView, ServicePaymentMixin):
	model = RoboAdvisorService
	template_name = "roboadvisor/steps/result.html"
	context_object_name = "service"

	# def manage_service_activity(self, status):
	# 	if 'service_activity' in self.request.session:
	# 		service_activity_id = self.request.session['service_activity']
	# 	if 'service_activity' in self.request.GET:
	# 		service_activity_id = self.request.GET['service_activity']

	# 	service_activity = RoboAdvisorUserServiceActivity.objects.get(id = service_activity_id)
	# 	service_activity.date_finished = datetime.datetime.now()
	# 	service_activity.status = status
	# 	service_activity.save(update_fields = ['date_finished', 'status'])
	# 	return service_activity

	# def service_payment(self):
	# 	user = self.request.user
	# 	service = self.object
	# 	user_credits = user.user_profile.creditos

	# 	if user_credits >= service.price:
	# 		user.update_credits(-service.price)
	# 		return self.manage_service_activity(1), True
	# 	else:
	# 		self.manage_service_activity(4)
	# 		difference = service.price - user_credits			
	# 		return difference, False

	# def return_results(self, service_activity):
	# 	user = self.request.user
	# 	if service_activity.service.slug == 'investor-profile':
	# 		result = get_investor_type(user, service_activity)
	# 	elif service_activity.service.slug == 'company-match':
	# 		result = RoboAdvisorQuestionCompanyAnalysis.objects.get(service_activity = service_activity).asset
	# 	return result

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	service_activity, validation = self.service_payment()
	# 	context['difference'] = service_activity
	# 	context["meta_title"] = 'Tu consejero inteligente'
	# 	if validation:
	# 		result = self.return_results(service_activity)
	# 		context['result'] = result
	# 		context['difference'] = None
		
	# 	return context
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		service_activity, validation = self.return_results()
		
		context['difference'] = service_activity
		context["meta_title"] = 'Tu consejero inteligente'
		if validation:
			context['difference'] = None
			context['result'] = service_activity
		
		return context


class RoboAdvisorUserResultsListView(ListView):
	model = RoboAdvisorUserServiceActivity
	template_name = "roboadvisor/own-results.html"
	context_object_name = "services"

	def get_queryset(self):
		return super().get_queryset().filter(user = self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["meta_desc"] = 'IA para mejorar las inversiones'
		context["meta_tags"] = 'finanzas, blog financiero, blog el financiera, invertir, roboadvisor'
		context["meta_title"] = 'Tu consejero inteligente'
		return context