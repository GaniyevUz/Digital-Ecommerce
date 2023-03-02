from django.urls import path
from ecommerce.views import ClientUpdateDestroyAPIView, CreateClientAPIView, ClientModelViewSet, ShopClientListAPIView

from django.shortcuts import get_object_or_404
from shops.models import Domain

urlpatterns = [
    path('sign-in', ClientModelViewSet.as_view({'get': 'get', 'post': 'post'}), name='sign-in'),
    path('sign-up', CreateClientAPIView.as_view(), name='sign-up'),
    path('profile/personal-info', ClientUpdateDestroyAPIView.as_view(), name='profile'),
    path('clients', ShopClientListAPIView.as_view(), name='client-list'),
]


def shop_exists_callback(request, subdomain):
    get_object_or_404(Domain, name=subdomain)
