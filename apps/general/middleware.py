import logging
import operator
import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import resolve, reverse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from apps.public_blog.urls import urlpatterns

from .utils import HostChecker

logger = logging.getLogger(__name__)
lower = operator.methodcaller('lower')

UNSET = object()


class SubdomainMiddleware(MiddlewareMixin):
    """
    A middleware class that adds a ``subdomain`` attribute to the current request.
    """
    def get_domain_for_request(self, request):
        """
        Returns the domain that will be used to identify the subdomain part
        for this request.
        """
        return HostChecker(request).current_site_domain()

    def process_request(self, request):
        """
        Adds a ``subdomain`` attribute to the ``request`` parameter.
        """
        domain, host = map(lower,
            (self.get_domain_for_request(request), request.get_host()))

        pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
        matches = re.match(pattern, host)

        if matches:
            request.subdomain = matches.group('subdomain')
        else:
            request.subdomain = None


class SubdomainURLRoutingMiddleware(SubdomainMiddleware):
    """
    A middleware class that allows for subdomain-based URL routing.
    """
    def process_request(self, request):
        super(SubdomainURLRoutingMiddleware, self).process_request(request)

        subdomain = getattr(request, 'subdomain', UNSET)
        if subdomain is not UNSET and subdomain is not None:
            current_url_name = resolve(request.path_info).url_name
            if (
                current_url_name in [url_name.name for url_name in urlpatterns]
                or current_url_name == 'inicio'
            ):
                return

            inicial_path = settings.FULL_DOMAIN
            full_path = request.get_full_path_info()
            return HttpResponseRedirect(f'{inicial_path}{full_path}')

    def process_response(self, request, response):
        """
        Forces the HTTP ``Vary`` header onto requests to avoid having responses
        cached across subdomains.
        """
        if getattr(settings, 'FORCE_VARY_ON_HOST', True):
            patch_vary_headers(response, ('Host',))
        return response