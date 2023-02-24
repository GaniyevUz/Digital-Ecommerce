from django.urls import path
from ecommerce.views import ClientUpdateDestroyAPIView, CreateClientAPIView, ClientModelViewSet

from django.shortcuts import get_object_or_404
from shops.models import Domain

urlpatterns = [
    path('sign-in', ClientModelViewSet.as_view({'get': 'get', 'post': 'post'})),
    path('sign-up', CreateClientAPIView.as_view()),
    path('profile/personal-info', ClientUpdateDestroyAPIView.as_view()),
]


def shop_exists_callback(request, subdomain):
    get_object_or_404(Domain, name=subdomain)
