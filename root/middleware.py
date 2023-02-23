from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin

from shops.models import Shop, Domain


class GetSubdomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domains = request.get_host().split('.')
        if domains:
            domain: str = domains[0]
            if domain in ['app', 'testserver']:
                return
            if domain.isidentifier():
                return get_object_or_404(Domain, name=domains)
        raise Http404('No Domain matches the given query.')
