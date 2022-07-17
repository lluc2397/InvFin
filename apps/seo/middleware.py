import logging
import operator

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .utils import SeoInformation

from django.contrib import auth

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

def get_visiteur(request):
    """
    Creates a new attribute, _cached_visiteur to the request object, 
    same as the user but for visitor
    """
    if not hasattr(request, "_cached_visiteur"):
        request._cached_visiteur = SeoInformation().find_visiteur(request)
    return request._cached_visiteur


class VisiteurMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``visiteur`` attribute to the current request.
    """


    def process_request(self, request):
        """
        Adds a ``visiteur`` attribute to the ``request`` parameter.
        """
        if not hasattr(request, "is_visiteur"):
            if request.user.is_authenticated:
                request.visiteur = None
                request.is_visiteur = False
            else:
                request.is_visiteur = True
                request.visiteur = SimpleLazyObject(lambda: get_visiteur(request))
