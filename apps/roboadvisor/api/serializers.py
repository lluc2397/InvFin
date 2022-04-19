from rest_framework.serializers import (
    StringRelatedField,
    ModelSerializer,
    FloatField,
    
)

from ..models import (
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorServiceStep,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorService,
    TemporaryInvestorProfile,
    InvestorProfile
)


# class BaseRoboAdvisorSerializer(ModelSerializer):
#     def create(self, validated_data: Any) -> _MT:
#         return super().create(validated_data)
    
#     def update(self, instance: _MT, validated_data: Any) -> _MT:
#         return super().update(instance, validated_data)

class RoboAdvisorQuestionCompanyAnalysisSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionCompanyAnalysis
        fields = '__all__'


class RoboAdvisorQuestionFinancialSituationSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionFinancialSituation
        fields = '__all__'


class RoboAdvisorQuestionInvestorExperienceSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionInvestorExperience
        fields = '__all__'


class RoboAdvisorQuestionPortfolioAssetsWeightSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionPortfolioAssetsWeight
        fields = '__all__'


class RoboAdvisorQuestionPortfolioCompositionSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionPortfolioComposition
        fields = '__all__'


class RoboAdvisorQuestionRiskAversionSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionRiskAversion
        fields = '__all__'


class RoboAdvisorQuestionStocksPortfolioSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionStocksPortfolio
        fields = '__all__'


