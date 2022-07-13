from django.conf import settings
from django.core.mail import send_mail

from config import celery_app

from .models import Superinvestor, SuperinvestorActivity
from .scrapper import get_activity, get_historial, get_investors_accronym


@celery_app.task()
def scrap_superinvestors():
    total_inv = get_investors_accronym()
    total = len(total_inv)
    list_of_all = ', '.join(total_inv)
    return send_mail('All investors scrapped', f'All {total} investors scrapped: {list_of_all}', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def scrap_superinvestors_activity(superinvestor_id):
    try:
        superinvestor = Superinvestor.objects.get(id=superinvestor_id)
        get_activity(superinvestor)
    except Exception as e:
        superinvestor.has_error = True
        superinvestor.error = e
        superinvestor.save(update_fields=['has_error', 'error'])


@celery_app.task()
def scrap_superinvestors_history(superinvestor_activity_id):
    try:
        superinvestor_activity = SuperinvestorActivity.objects.get(id=superinvestor_activity_id)
        get_historial(superinvestor_activity)
    except Exception as e:
        superinvestor_activity.superinvestor_related.has_error = True
        superinvestor_activity.superinvestor_related.error = e
        superinvestor_activity.superinvestor_related.save(update_fields=['has_error', 'error'])
    

@celery_app.task()
def prepare_scrap_superinvestors_activity():
    for superinvestor in Superinvestor.objects.all():
        scrap_superinvestors_activity.delay(superinvestor.id)
    send_mail('All activity done', f'All activity done', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])
    return 'finished'


@celery_app.task()
def prepare_scrap_superinvestors_history():
    for superinvestor in SuperinvestorActivity.objects.filter(need_verify_company=False):
        scrap_superinvestors_history.delay(superinvestor.id)
    send_mail('All activity done', f'All activity done', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])
    return 'finished'