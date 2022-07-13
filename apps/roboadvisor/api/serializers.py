from rest_framework.serializers import FloatField, ModelSerializer, StringRelatedField

from ..models import (
    InvestorProfile,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,
    RoboAdvisorService,
    RoboAdvisorServiceStep,
    TemporaryInvestorProfile,
)


class BaseRoboAdvisorSerializer(ModelSerializer):
    def create(self, validated_data):
        instance = super().create(validated_data)
        

        instance.service_activity
        instance.service_step
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class RoboAdvisorQuestionCompanyAnalysisSerializer(ModelSerializer):
    class Meta:
        model = RoboAdvisorQuestionCompanyAnalysis
        fields = '__all__'
    
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.asset
        instance.result
        instance.save()
        return instance


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


