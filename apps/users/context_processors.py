from django.conf import settings
from apps.general.models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()


def users_notifications(request):
    user = request.user
    count_notifications=0
    user_notifs = None
    if user.is_authenticated:
        count_notifications = Notification.objects.filter(user = user, is_seen=False).count()
        user_notifs = Notification.objects.filter(user = user).order_by("-date")
    return {'count_notifications' : count_notifications, 'user_notifs': user_notifs}


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def user_companies_visited(request):
    companies_visited = [] 
    if 'companies_visited' in request.session:
        companies_visited = request.session['companies_visited']
    return {'companies_visited': companies_visited}