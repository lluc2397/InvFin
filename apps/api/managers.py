from django.db.models import Manager

from apps.general.managers import BaseSharedManager

class KeyManager(Manager, BaseSharedManager):

    def key_is_active(self, key):
        return self.filter(key=key, in_use=True).exists()
    
    def cuota_remainig(self, key):
        from .models import CompanyRequestAPI, TermRequestAPI
        companies = CompanyRequestAPI.objects.count_use_today(key)
        terms = TermRequestAPI.objects.count_use_today(key)
        limit = self.get(key=key, in_use=True).limit
        total_requests = companies + terms
        return limit - total_requests

    def key_authorized(self, key):
        return self.key_is_active(key) is True \
            and self.cuota_remainig(key) > 0

    