from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shops.views.shop_belongs import TelegramBotModelViewSet
from products.views import CategoryModelViewSet as ProductCategoryModelViewSet, ProductModelViewSet
from shops.views import ShopModelViewSet, CurrencyModelViewSet, PaymentProvidersViewSet, CategoryModelViewSet

router = DefaultRouter()
router.register('shop', ShopModelViewSet, 'shop')
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')
router.register('payment', PaymentProvidersViewSet, 'payment')

list_ = {'get': 'list', 'post': 'create'}
urlpatterns = [
    # path('shop/<int:pk>/order', ShopOrdersRetrieveAPIView.as_view(), name='orders'),
    path('', include(router.urls)),
    path('shop/<int:pk>/bot', TelegramBotModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),
    path('shop/<int:pk>/product', ProductModelViewSet.as_view(list_), name='product-list'),
    path('shop/<int:pk>/category', ProductCategoryModelViewSet.as_view(list_), name='category-list')
]
