from django.forms import (
    ModelForm,
)

from .models import (
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,
)


class BaseRoboAdvisorForm(ModelForm):
    def range_values(self, name, min = 0, max = 100, step = 10):
        attrs = {
            'min':f"{min}",
            'max':f"{max}",
            'step':f"{step}",
            'onInput':f"$('#{name}').html($(this).val())"
        }
        return attrs

class RoboAdvisorQuestionInvestorExperienceForm(BaseRoboAdvisorForm):
    
    def __init__(self, *args, **kwargs):
        super(RoboAdvisorQuestionInvestorExperienceForm, self).__init__(*args, **kwargs)
        self.fields['percentage_invested'].widget.attrs.update(
            self.range_values('rangeval6', step = 1)
            )
        self.fields['percentage_anualized_revenue'].widget.attrs.update(
            self.range_values('rangeval7', max = 1000, step = 0.1)
            )

    class Meta:
        model = RoboAdvisorQuestionInvestorExperience
        fields = '__all__'
        exclude = []
        # labels = {
        #     'age': ('Textodeayuda'),
        #     'objectif': ('Textodeayuda'),
        #     'investor_type_self_definition': ('Textodeayuda'),
        #     'percentage_invested': ('Textodeayuda'),
        #     'percentage_anualized_revenue': ('Textodeayuda'),
        #     'years_investing': ('Textodeayuda'),
        # }
        # help_texts = {
        #     'age': ('Textodeayuda'),
        #     'objectif': ('Textodeayuda'),
        #     'investor_type_self_definition': ('Textodeayuda'),
        #     'percentage_invested': ('Textodeayuda'),
        #     'percentage_anualized_revenue': ('Textodeayuda'),
        #     'years_investing': ('Textodeayuda'),
        # }



class RoboAdvisorQuestionCompanyAnalysisForm(BaseRoboAdvisorForm):

    class Meta:
        model = RoboAdvisorQuestionCompanyAnalysis
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionFinancialSituationForm(BaseRoboAdvisorForm):
    class Meta:
        model = RoboAdvisorQuestionFinancialSituation
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionRiskAversionForm(BaseRoboAdvisorForm):

    def __init__(self, *args, **kwargs):
        super(RoboAdvisorQuestionRiskAversionForm, self).__init__(*args, **kwargs)
        # self.fields['volatilidad'].widget.attrs = {'my_attribute_key':'my_attribute_value'}
        self.fields['percentage_for_onefive'].widget.attrs.update(self.range_values('rangeval'))
        self.fields['percentage_for_three'].widget.attrs.update(self.range_values('rangeval2'))
        self.fields['percentage_for_fourfive'].widget.attrs.update(self.range_values('rangeval3'))
        self.fields['percentage_for_zerofive'].widget.attrs.update(self.range_values('rangeval4'))
        self.fields['percentage_in_one_stock'].widget.attrs.update(self.range_values('rangeval5'))
    #     self.fields['number_stocks'].widget.attrs
    #     self.fields['age'].label = 'Texto de aydua'

    class Meta:
        model = RoboAdvisorQuestionRiskAversion
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionPortfolioAssetsWeightForm(BaseRoboAdvisorForm):
    class Meta:
        model = RoboAdvisorQuestionPortfolioAssetsWeight
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionStocksPortfolioForm(BaseRoboAdvisorForm):
    class Meta:
        model = RoboAdvisorQuestionStocksPortfolio
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionPortfolioCompositionForm(BaseRoboAdvisorForm):
    class Meta:
        model = RoboAdvisorQuestionPortfolioComposition
        fields = '__all__'
        exclude = []



# class CompanyMatch
#RoboAdvisorQuestionInvestorExperience
#RoboAdvisorQuestionCompanyAnalysis



# class OptimizePortfolioAccordingToProfile
#RoboAdvisorQuestionInvestorExperience
#RoboAdvisorQuestionRiskAversion
#RoboAdvisorQuestionStocksPortfolio
#RoboAdvisorQuestionPortfolioComposition
