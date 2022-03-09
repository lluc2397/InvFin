from apps.general.utils import HostChecker

class HostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # if HostChecker.correct_host(request) == False:
        #     current_domain = Site.objects.get_current().domain
        #     print(request.get_full_path_info())
        #     print('*'*100)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class SubdomainMiddleware:
    """ Make the subdomain publicly available to classes """
    
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0]
            if (subdomain.lower() == 'www'):
                subdomain = None
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = None
            domain = request.get_host()
        
        request.subdomain = subdomain
        request.domain = domain

# class SubdomainMiddleware(object):
#     """
#     A middleware class that adds a ``subdomain`` attribute to the current request.
#     """
#     def get_domain_for_request(self, request):
#         """
#         Returns the domain that will be used to identify the subdomain part
#         for this request.
#         """
#         return get_domain()

#     def process_request(self, request):
#         """
#         Adds a ``subdomain`` attribute to the ``request`` parameter.
#         """
#         domain, host = map(lower,
#             (self.get_domain_for_request(request), request.get_host()))

#         pattern = r'^(?:(?P<subdomain>.*?)\.)?%s(?::.*)?$' % re.escape(domain)
#         matches = re.match(pattern, host)

#         if matches:
#             request.subdomain = matches.group('subdomain')
#         else:
#             request.subdomain = None
#             logger.warning('The host %s does not belong to the domain %s, '
#                 'unable to identify the subdomain for this request',
#                 request.get_host(), domain)