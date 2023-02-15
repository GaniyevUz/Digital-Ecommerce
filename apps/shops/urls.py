from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderModelViewSet
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
    path('', include(router.urls)),
    path('shop/<int:shop>/bot', TelegramBotModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),
    path('shop/<int:shop>/product', ProductModelViewSet.as_view(list_), name='product-list'),
    path('shop/<int:shop>/category', ProductCategoryModelViewSet.as_view(list_), name='category-list'),
    path('shop/<int:shop>/category', ProductCategoryModelViewSet.as_view(list_), name='order-list'),
    path('shop/<int:shop>/order', OrderModelViewSet.as_view(list_), name='order-list'),
]
