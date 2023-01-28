from django.urls import path

from apps.shops.views.shop import ShopListCreateAPIView
from shops.views.shop import ShopRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('shop', ShopListCreateAPIView.as_view(), name='shop'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='detail')
]
