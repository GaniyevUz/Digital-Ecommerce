from django_hosts import patterns, host

from root import settings

host_patterns = patterns(
    'root',
    host(r'app', 'urls', 'app'),
    host(r'(\w+)', 'other_urls', 'other'),
)

if settings.DEBUG:
    host_patterns.insert(
        0, host(r'testserver', 'urls', 'testserver')
    )
