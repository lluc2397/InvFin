import logging
import operator

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from .utils import SeoInformation

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')


class VisiteurMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``visiteur`` attribute to the current request.
    """

    def get_visiteur(self, request):
        """
        Creates a new attribute, _cached_visiteur to the request object, 
        same as the user but for visitor
        """
        if not hasattr(request, "_cached_visiteur"):
            request._cached_visiteur = SeoInformation().find_visiteur(request)
        return request._cached_visiteur

    def process_request(self, request):
        """
        Adds a ``visiteur`` attribute to the ``request`` parameter.
        """
        if request.user.is_authenticated:
            request.visiteur = None
            request.is_visiteur = False
        else:
            request.is_visiteur = True
            request.visiteur = SimpleLazyObject(self.get_visiteur(request))
