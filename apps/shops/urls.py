from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.shops.views.shop import ShopListCreateAPIView
from shops.views.shop import ShopRetrieveUpdateDestroyAPIView
from shops.views.shop_belongs import CategoryModelViewSet, CurrencyModelViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')

urlpatterns = [
    path('', include(router.urls)),
    path('shop', ShopListCreateAPIView.as_view(), name='shop'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='detail')
]
