from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shops.views import ShopModelViewSet, CategoryModelViewSet, \
    CurrencyModelViewSet, PaymentProvidersViewSet
from shops.views.shop_belongs import TelegramBotModelViewSet

router = DefaultRouter()
router.register('shop', ShopModelViewSet, 'shop')
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')
router.register('payment', PaymentProvidersViewSet, 'payment')

urlpatterns = [
    # path('shop/<int:pk>/order', ShopOrdersRetrieveAPIView.as_view(), name='orders'),
    path('', include(router.urls)),
    path('shop/<int:pk>/bot', TelegramBotModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot')
]
