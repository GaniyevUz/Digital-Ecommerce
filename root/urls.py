from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from root import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="BotCommerce.io API",
        default_version='v1',
        description="A complete shop, with payment systems, delivery services and convenient control panel with "
                    "built-in CRM and Analytics.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/v1/', include('apps.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
