from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shops.views import ShopListCreateAPIView, ShopRetrieveUpdateDestroyAPIView, CategoryModelViewSet, CurrencyModelViewSet, PaymentProvidersViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')
router.register('payment', PaymentProvidersViewSet, 'payment')

urlpatterns = [
    path('shop', ShopListCreateAPIView.as_view(), name='shop'),
    path('shop/<int:pk>/detail', ShopRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
    path('', include(router.urls)),
]
