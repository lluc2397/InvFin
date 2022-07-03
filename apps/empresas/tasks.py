from config import celery_app
from datetime import datetime

from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail

from .models import Company
from .company.update import UpdateCompany


@celery_app.task()
def update_institutionals_info_company_task():
    org_name = 'Estados Unidos'
    companies_without_info = Company.objects.clean_companies_by_main_exchange(org_name)
    intento = 0
    for company in companies_without_info:
        if intento == 5:
            return
        if company.checkings['has_institutionals']['state'] == 'no':
            update = UpdateCompany(company).institutional_ownership
            if update == 'all right':
                intento += 1
                company.modify_checkings('has_meta_image', 'yes')


@celery_app.task()
def update_basic_info_company_task():
    companies_without_info = Company.objects.filter(Q(has_logo=False) | Q(description_translated=False))
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).general_update()
    else:
        return send_mail('No companies left', 'All companies have info', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def save_remote_images_company_task():
    companies_without_info = Company.objects.filter(has_logo=True, exchange__main_org__name='Estados Unidos')
    if companies_without_info.exists():
        company = companies_without_info.first()
        if company.has_meta_image is False:
            return UpdateCompany(company).save_logo_remotely()
    else:
        return send_mail('No companies left', 'All companies have images', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def update_company_financials_task():
    org_name = 'Estados Unidos'
    companies_without_info = Company.objects.clean_companies_to_update(org_name).filter(date_updated=False)
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).financial_update()
    else:
        return send_mail('No companies left to update financials', f'All companies have info for {org_name}', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])
