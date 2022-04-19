from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    RoboAdvisorQuestionCompanyAnalysisSerializer,
    RoboAdvisorQuestionFinancialSituationSerializer,
    RoboAdvisorQuestionInvestorExperienceSerializer,
    RoboAdvisorQuestionPortfolioAssetsWeightSerializer,
    RoboAdvisorQuestionPortfolioCompositionSerializer,
    RoboAdvisorQuestionRiskAversionSerializer,
    RoboAdvisorQuestionStocksPortfolioSerializer
)

class BaseRoboAdvisorAPIView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    def post(self, request, ses):
        if request.session[ses]:
            response = self.update(request)
            response(status=status.HTTP_200_OK)

        else:
            response = self.create(request)
            request.session[ses] = 'created'
            
        return response


class RoboAdvisorQuestionCompanyAnalysisAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionCompanyAnalysisSerializer

    def post(self, request, ses='company-analysis'):
        return super().post(request, ses)


class RoboAdvisorQuestionFinancialSituationAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionFinancialSituationSerializer

    def post(self, request, ses='financial-situation'):
        return super().post(request, ses)


class RoboAdvisorQuestionInvestorExperienceAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionInvestorExperienceSerializer

    def post(self, request, ses='experience'):
        return super().post(request, ses)


class RoboAdvisorQuestionPortfolioAssetsWeightAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionPortfolioAssetsWeightSerializer

    def post(self, request, ses='assests-weight'):
        return super().post(request, ses)


class RoboAdvisorQuestionPortfolioCompositionAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionPortfolioCompositionSerializer

    def post(self, request, ses='portfolio-composition'):
        return super().post(request, ses)


class RoboAdvisorQuestionRiskAversionAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionRiskAversionSerializer

    def post(self, request, ses='risk-aversion'):
        return super().post(request, ses)


class RoboAdvisorQuestionStocksPortfolioAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionStocksPortfolioSerializer

    def post(self, request, ses='stocks-portfolio'):
        return super().post(request, ses)

