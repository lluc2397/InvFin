from django.db.models import Manager
from apps.super_investors.models import Period

class SuperinvestorManager(Manager):
    current_period = Period.objects.earliest()
    
    def current_positions(self, pk):        
        return self.get(id=pk).history.filter(period_related=self.current_period)
    
    def resume_current_positions(self):
        pass

    def all_buys(self):
        pass

    def all_sells(self):
        pass

    
class SuperinvestorHistoryManager(Manager):
    current_period = Period.objects.earliest()

    def company_in_current_portfolios(self, company_id):
        return self.filter(period_related=self.current_period, company_id=company_id)