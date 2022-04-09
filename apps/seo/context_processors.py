from .models import (
    VisiteurJourney,
    UsersJourney
)
from .utils import SeoInformation
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

def journey(request):
    current_path = request.META['PATH_INFO']
    comes_from = str(request.META.get('HTTP_REFERER'))

    if request.user.is_authenticated and request.user.username != 'Lucas':
        UsersJourney.objects.create(user = request.user, current_path = current_path, comes_from = comes_from)

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