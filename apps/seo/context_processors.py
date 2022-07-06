from .models import (
    VisiteurJourney,
    UsersJourney
)
from .utils import SeoInformation
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

def journey(request):
    current_path = request.build_absolute_uri()
    comes_from = str(request.META.get('HTTP_REFERER'))
    request_visiteur = getattr(request, 'visiteur', None)
    if not request_visiteur:
        setattr(request, 'visiteur', {'is_visiteur': False})
    if request.user.is_authenticated and request.user.username != 'Lucas':
        UsersJourney.objects.create(user = request.user, current_path = current_path, comes_from = comes_from)

    if request.user.is_anonymous:
        try:
            visiteur = SeoInformation().find_visiteur(request)
            request_visiteur.update({'visiteur': visiteur, 'is_visiteur': True})
            VisiteurJourney.objects.create(user = visiteur, current_path = current_path, comes_from = comes_from)        
        except Exception as e:
            print(e, 'context seo')
    
    return {}

def debug(request):
    debug = settings.DEBUG
    return {'debug':debug}