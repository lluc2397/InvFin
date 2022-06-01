from ntpath import join
from config import celery_app

from django.core.mail import send_mail
from django.conf import settings

from .models import Superinvestor
from .scrapper import get_investors_accronym, get_activity


@celery_app.task()
def scrap_superinvestors():
    total_inv = get_investors_accronym()
    total = len(total_inv)
    list_of_all = ', '.join(total_inv)
    return send_mail('All investors scrapped', f'All {total} investors scrapped: {list_of_all}', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def scrap_superinvestors_activity():
    for superinvestor in Superinvestor.objects.all():
        try:
            get_activity(superinvestor)
        except Exception as e:
            superinvestor.has_error = True
            superinvestor.error = e
            superinvestor.save(update_fields=['has_error', 'error'])
    return send_mail('All activity done', f'All activity done', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])