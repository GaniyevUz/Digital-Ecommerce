from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shops.views import ShopModelViewSet, CategoryModelViewSet, \
    CurrencyModelViewSet, PaymentProvidersViewSet

router = DefaultRouter()
router.register('shop', ShopModelViewSet, 'shop')
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')
router.register('payment', PaymentProvidersViewSet, 'payment')

urlpatterns = [
    # path('shop/<int:pk>/order', ShopOrdersRetrieveAPIView.as_view(), name='orders'),
    path('', include(router.urls)),
]
