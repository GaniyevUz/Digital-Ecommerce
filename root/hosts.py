from django_hosts import patterns, host

from root import settings

host_patterns = patterns(
    'root',
    host(r'app', 'urls', 'app'),
    host(r'(\w+)', 'other_urls', 'other'),  # for any subdomain
)

if settings.DEBUG:
    host_patterns.append(host(r'test', 'other_urls', 'other'))  # only for any testing
