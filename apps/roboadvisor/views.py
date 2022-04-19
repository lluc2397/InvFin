from django.shortcuts import render
from django.views.generic import (
	ListView,
	TemplateView,
	DetailView)

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
	RoboAdvisorQuestionRiskAversionForm,
	RoboAdvisorQuestionStocksPortfolioForm
)

from .constants import (
	PERIODS,
	KNOWLEDGE,
	INVESTOR_TYPE,
	NUMBER_STOCKS,
	OBJECTIFS
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

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		service = self.get_object()

		context["meta_title"] = f'{service.title}'
		context["meta_url"] = f'/robo-option/{service.slug}/'

		context["experience_form"] = RoboAdvisorQuestionInvestorExperienceForm()
		context["company_analysis_form"] = RoboAdvisorQuestionCompanyAnalysisForm()
		context["financial_situation_form"] = RoboAdvisorQuestionFinancialSituationForm()
		context["risk_aversion_form"] = RoboAdvisorQuestionRiskAversionForm()
		context["assets_weight_form"] = RoboAdvisorQuestionPortfolioAssetsWeightForm()
		context["portfolio_asset_form"] = RoboAdvisorQuestionPortfolioCompositionForm()

		default_data = {
			'user': self.request.user,
			'service': service
		}
		test_activity = RoboAdvisorUserServiceActivity.objects.create(**default_data)

		self.request.session['test-activity'] = test_activity.id

		return context
