from config import celery_app

from .models import Company
from .utils import UpdateCompany


@celery_app.task()
def update_basic_info_company_task():
    for company in Company.objects.filter(date_updated = False):
        return UpdateCompany(company).full_general_updates()


@celery_app.task()
def update_company_financials_task():
    for company in Company.objects.filter(updated = False):
        return UpdateCompany(company).check_last_filing()