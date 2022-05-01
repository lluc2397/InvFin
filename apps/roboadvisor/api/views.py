from django.contrib.auth import get_user_model

from rest_framework.generics import GenericAPIView

from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework import status

from apps.empresas.brain.analysis import simple_stock_analysis
from apps.empresas.models import Company

from .serializers import (
    RoboAdvisorQuestionCompanyAnalysisSerializer,
    RoboAdvisorQuestionFinancialSituationSerializer,
    RoboAdvisorQuestionInvestorExperienceSerializer,
    RoboAdvisorQuestionPortfolioAssetsWeightSerializer,
    RoboAdvisorQuestionPortfolioCompositionSerializer,
    RoboAdvisorQuestionRiskAversionSerializer,
    RoboAdvisorQuestionStocksPortfolioSerializer
)

from ..models import (
    RoboAdvisorUserServiceStepActivity,
    RoboAdvisorServiceStep,
    RoboAdvisorUserServiceActivity,
    RoboAdvisorQuestionCompanyAnalysis,
    RoboAdvisorQuestionFinancialSituation,
    RoboAdvisorQuestionInvestorExperience,
    RoboAdvisorQuestionPortfolioAssetsWeight,
    RoboAdvisorQuestionPortfolioComposition,
    RoboAdvisorQuestionRiskAversion,
    RoboAdvisorQuestionStocksPortfolio,

)

from ..constants import *

User = get_user_model()


class BaseRoboAdvisorAPIView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    def create(self, data):
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, headers=headers)

    def post(self, request, ses):
        client_side_data = request.data.dict()

        user = User.objects.get(id = client_side_data['user'])
        service_step = RoboAdvisorUserServiceStepActivity.objects.create(
            user = user,
            step = RoboAdvisorServiceStep.objects.get(id = client_side_data['step']),
            date_started = client_side_data['date_started'],
            status = "finished",
        )

        user_activity = {
            'service_activity': client_side_data['service_activity'],
            'service_step': service_step.pk
        }
        

        if ses == 'company-analysis':
            asset = Company.objects.get(ticker = client_side_data['stock'].split(' (')[1][:-1])
            result = simple_stock_analysis(asset)

            client_side_data['result'] = result['result']
            client_side_data['asset'] = asset.pk

            # session['company-analysis-result'] = result
            # session.modified = True

        client_side_data.update(user_activity)
        # if ses in session:
        #     response = self.update(client_side_data)
        #     response(status=status.HTTP_200_OK)

        # else:
        #     response = self.create(client_side_data)
        #     session[ses] = 'created'
        
        # if 'final' in request.COOKIES and request.COOKIES['final'] == True:
        #     request.session.clear()
        # print(client_side_data)
        response = self.create(client_side_data)
        
        return response


class RoboAdvisorQuestionCompanyAnalysisAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionCompanyAnalysisSerializer
    queryset = RoboAdvisorQuestionCompanyAnalysis.objects.all()

    def post(self, request, ses='company-analysis'):
        return super().post(request, ses)


class RoboAdvisorQuestionFinancialSituationAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionFinancialSituationSerializer
    queryset = RoboAdvisorQuestionFinancialSituation.objects.all()

    def post(self, request, ses='financial-situation'):
        return super().post(request, ses)


class RoboAdvisorQuestionInvestorExperienceAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionInvestorExperienceSerializer
    queryset = RoboAdvisorQuestionInvestorExperience.objects.all()

    def post(self, request, ses='experience'):
        return super().post(request, ses)


class RoboAdvisorQuestionPortfolioAssetsWeightAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionPortfolioAssetsWeightSerializer
    queryset = RoboAdvisorQuestionPortfolioAssetsWeight.objects.all()

    def post(self, request, ses='assests-weight'):
        return super().post(request, ses)


class RoboAdvisorQuestionRiskAversionAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionRiskAversionSerializer
    queryset = RoboAdvisorQuestionRiskAversion.objects.all()

    def post(self, request, ses='risk-aversion'):
        return super().post(request, ses)


class RoboAdvisorQuestionPortfolioCompositionAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionPortfolioCompositionSerializer
    queryset = RoboAdvisorQuestionPortfolioComposition.objects.all()

    def post(self, request, ses='portfolio-composition'):
        return super().post(request, ses)


class RoboAdvisorQuestionStocksPortfolioAPIView(BaseRoboAdvisorAPIView):
    serializer_class = RoboAdvisorQuestionStocksPortfolioSerializer
    queryset = RoboAdvisorQuestionStocksPortfolio.objects.all()

    def post(self, request, ses='stocks-portfolio'):
        return super().post(request, ses)

