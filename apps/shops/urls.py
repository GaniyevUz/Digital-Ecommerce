from django.urls import path

from apps.shops.views.shop import ShopCreateListAPIView
from shops.views.shop import ShopRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('shop', ShopCreateListAPIView.as_view(), name='shop'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='detail')
]
