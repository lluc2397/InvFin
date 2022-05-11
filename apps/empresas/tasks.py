from config import celery_app

from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from .models import Company
from .company.update import UpdateCompany


@celery_app.task()
def update_basic_info_company_task():
    companies_without_info = Company.objects.filter(Q(has_logo=False) | Q(description_translated=False))
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).general_update()
    else:
        return send_mail('No companies left', 'All companies have info', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def update_company_financials_task():
    org_name = 'Estados Unidos'
    companies_without_info = Company.objects.filter(exchange__main_org__name = org_name, updated = False)
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).financial_update()
    else:
        return send_mail('No companies left to update financials', f'All companies have info for {org_name}', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])
