from django_hosts import patterns, host

host_patterns = patterns(
    'root',
    host(r'api', 'urls', 'api'),
    host(r'(?P<subdomain>\w+)', 'other_urls', 'other', 'ecommerce.urls.shop_exists_callback'),
)