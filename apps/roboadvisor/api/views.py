import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework import status

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
    RoboAdvisorUserServiceStepActivity
)


class BaseRoboAdvisorAPIView(GenericAPIView, CreateModelMixin, UpdateModelMixin):

    def post(self, request, ses):
        client_side_data = request.data
        session = self.request.session
        # if 'first-step' in session and session['first-step']['used'] == False:
        #     service_step = RoboAdvisorUserServiceStepActivity.objects.get(id = session['first-step']['id'])
        #     service_step.date_finished = datetime.datetime.now()
        #     service_step.save()
        #     session['first-step']['used'] = True
        # else:
        service_step = RoboAdvisorUserServiceStepActivity.objects.create(
            user = self.request.user,
            step__id = client_side_data['step__id'],
            date_started = client_side_data['date_started'],
            status = 1,
        )
            

        user_activity = {
            'service_activity__id': session['test-activity'],
            'service_step': service_step
        }
        

        if ses == 'company-analysis':
            asset = Company.objects.get(ticker = client_side_data['stock'].split(' (')[1][:-1])
            result = ''
            client_side_data['asset'] = asset


        client_side_data.update(user_activity)
        if ses in session:
            response = self.update(client_side_data)
            response(status=status.HTTP_200_OK)

        else:
            response = self.create(client_side_data)
            session[ses] = 'created'
            
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

