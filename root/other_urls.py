from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from root import settings

urlpatterns = [
    path('api/v1/ecommerce/', include(('apps.urls', 'apps'), 'api')),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="BotCommerce.io API for Ecommerce",
            default_version='v1',
            description="A complete shop, with payment systems, delivery services and convenient control panel with "
                        "built-in CRM and Analytics.",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact('GitHub Repository', 'https://github.com/GaniyevUz/BotCommerce'),
            license=openapi.License(name='MIT License'),
        ),
        public=True,
        patterns=urlpatterns,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns += [
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
