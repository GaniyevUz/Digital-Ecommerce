from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from shops.models import Domain


class GetSubdomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domains = request.get_host().split('.')
        if len(domains) >= 2:  # subdomain.example.com
            domain: str = domains[0]
            if domain in ['app', 'test'] and domain.isidentifier():
                return
            get_object_or_404(Domain, name=domain)
