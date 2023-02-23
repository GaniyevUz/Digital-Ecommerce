from django.http import Http404
from django.utils.deprecation import MiddlewareMixin


class GetSubdomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domains = request.get_host().split('.')
        if len(domains) and domains[0] == 'app':
            raise Http404
