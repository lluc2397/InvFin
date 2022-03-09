from django.contrib.sites.models import Site

from apps.public_blog.models import WritterProfile


class HostChecker:
    def __init__(self, request) -> None:
        self.request = request
        self.host = self.request.get_host().split('.')[0]
        self.current_domain = Site.objects.get_current().domain
    

    def check_writter(self):
        if WritterProfile.objects.filter(host_name = self.host).exists():
            return self.host
        else:
            return False
    
    def check_host(self):
        if self.host != self.current_domain and self.host != "www":
            return False
    
    def correct_host(self):
        if self.check_host() == False and self.check_writter == False:
            return f'http://{self.current_domain}'


class Votes:
    pass

class Reputation:
    pass