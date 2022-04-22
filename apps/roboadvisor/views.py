import datetime

from django.views.generic import (
	ListView,
	TemplateView,
	DetailView)

from .models import (
    RoboAdvisorService,
	RoboAdvisorUserServiceActivity,
	RoboAdvisorUserServiceStepActivity
)

from .forms import (
	RoboAdvisorQuestionInvestorExperienceForm,
	RoboAdvisorQuestionCompanyAnalysisForm,
	RoboAdvisorQuestionFinancialSituationForm,
	RoboAdvisorQuestionPortfolioAssetsWeightForm,
	RoboAdvisorQuestionPortfolioCompositionForm,
	RoboAdvisorQuestionRiskAversionForm,
	RoboAdvisorQuestionStocksPortfolioForm
)

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


class RoboAdvisorResultView(TemplateView):
	template_name = "roboadvisor/steps/result.html"

	def finish_service_activity(self):
		service_activity = RoboAdvisorUserServiceActivity.objects.get(id = self.request.session['service_activity'])
		# service_activity.date_finished = datetime.datetime.now()
		# service_activity.status = 1
		# service_activity.save(update_fields = ['date_finished', 'status'])
		return service_activity

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['service_activity'] = self.finish_service_activity()

		return context