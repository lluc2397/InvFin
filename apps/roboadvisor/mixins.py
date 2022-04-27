import datetime

from .models import RoboAdvisorUserServiceActivity
from .brain.investor import get_investor_type

class ServicePaymentMixin:
    def get_service_activity(self):
        """
        After means that the user has already finished the test and wants to get the results from his profile. 
        """
        if 'before_service_activity' in self.request.GET:
            service_activity_id = self.request.GET['before_service_activity']
            moment = 'before'
        
        if 'after_service_activity' in self.request.GET:
            service_activity_id = self.request.GET['after_service_activity']
            moment = 'after'

        return RoboAdvisorUserServiceActivity.objects.get(id = service_activity_id), moment

        # elif service_activity.status == 'abandoned':# Abandoned
        #     return self.service_payment(service_activity)

        # elif service_activity.status == 'started':# Started
        #     return self.service_payment(service_activity)

    def manage_service_activity(self, service_activity, status):
        if service_activity.status != status:
            service_activity.date_finished = datetime.datetime.now()
            service_activity.status = status
            service_activity.save(update_fields = ['date_finished', 'status'])
        return service_activity.service_result

    def service_payment(self, user, service_activity):
        service = self.get_object()
        user_credits = user.user_profile.creditos

        if user_credits >= service.price:
            user.update_credits(-service.price)
            return self.manage_service_activity(service_activity, 'finished'), True
        else:
            self.manage_service_activity(service_activity, 'not-payed')
            difference = service.price - user_credits			
            return difference, False

    def return_results(self):
        user = self.request.user
        service_activity, moment = self.get_service_activity()

        if moment == 'before' and service_activity.service.slug == 'investor-profile':
            get_investor_type(user, service_activity)
        
        return self.service_payment(user, service_activity)
