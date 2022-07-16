from django.conf import settings
from django.contrib.auth import get_user_model

from .models import UserJourney, VisiteurJourney
from .utils import SeoInformation

User = get_user_model()


def journey(request):
    current_path = request.build_absolute_uri()
    comes_from = str(request.META.get('HTTP_REFERER'))
    
    
    if request.user.is_authenticated and request.user.username != 'Lucas':
        UserJourney.objects.create(user = request.user, current_path = current_path, comes_from = comes_from)

    if request.user.is_anonymous:
        try:
            visiteur = SeoInformation().find_visiteur(request)
            VisiteurJourney.objects.create(user = visiteur, current_path = current_path, comes_from = comes_from)        
        except Exception as e:
            print(e, 'context seo')
    
    return {}

def debug(request):
    debug = settings.DEBUG
    return {'debug':debug}