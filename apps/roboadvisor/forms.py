from django.forms import (
    ModelForm,
    CharField,
    DateTimeField,
    Form,
    IntegerField,
    Textarea,
    TextInput
)

from .models import (
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorQuestionPortfolioComposition,
)


# class BaseRoboAdvisorForm(ModelForm):


class RoboAdvisorQuestionInvestorExperienceForm(ModelForm):
    
    # def __init__(self, *args, **kwargs):
    #     super(RoboAdvisorQuestionInvestorExperienceForm, self).__init__(*args, **kwargs)
    #     self.fields['age'].label = 'Texto de aydua'
    #     self.fields['objectif'].label = 'Texto de aydua'
    #     self.fields['investor_type_self_definition'].label = 'Texto de aydua'
    #     self.fields['percentage_invested'].label = 'Texto de aydua'
    #     self.fields['percentage_anualized_revenue'].label = 'Texto de aydua'
    #     self.fields['years_investing'].label = 'Texto de aydua'


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



class RoboAdvisorQuestionCompanyAnalysisForm(ModelForm):

    class Meta:
        model = RoboAdvisorQuestionCompanyAnalysis
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionFinancialSituationForm(ModelForm):
    class Meta:
        model = RoboAdvisorQuestionFinancialSituation
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionRiskAversionForm(ModelForm):
    class Meta:
        model = RoboAdvisorQuestionRiskAversion
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionPortfolioAssetsWeightForm(ModelForm):
    class Meta:
        model = RoboAdvisorQuestionPortfolioAssetsWeight
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionStocksPortfolioForm(ModelForm):
    class Meta:
        model = RoboAdvisorQuestionStocksPortfolio
        fields = '__all__'
        exclude = []


class RoboAdvisorQuestionPortfolioCompositionForm(ModelForm):
    class Meta:
        model = RoboAdvisorQuestionPortfolioComposition
        fields = '__all__'
        exclude = []





# class CompanyMatch
#RoboAdvisorQuestionInvestorExperience
#RoboAdvisorQuestionCompanyAnalysis


# class UserInvestorProfile
#RoboAdvisorQuestionFinancialSituation
#RoboAdvisorQuestionInvestorExperience
#RoboAdvisorQuestionRiskAversion
#RoboAdvisorQuestionPortfolioAssetsWeight


# class OptimizePortfolioAccordingToProfile
#RoboAdvisorQuestionInvestorExperience
#RoboAdvisorQuestionRiskAversion
#RoboAdvisorQuestionStocksPortfolio
#RoboAdvisorQuestionPortfolioComposition
