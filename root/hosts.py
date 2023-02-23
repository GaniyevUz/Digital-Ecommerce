from django_hosts import patterns, host

host_patterns = patterns('root',
    host(r'app', 'urls', 'app'),
    host(r'(\w+)', 'other_urls', 'other'),
)
