from django.urls import path, include

from orders.views import OrderModelViewSet
from products.views import CategoryModelViewSet as ProductCategoryModelViewSet, ProductModelViewSet, \
    ProductCategoryMoveAPI
from shared.routers import BotCommerceRouter
from shops.views import ShopModelViewSet, CurrencyModelViewSet, PaymentProvidersViewSet, CategoryModelViewSet, StatShop
from shops.views.shop_belongs import TelegramBotModelViewSet

router = BotCommerceRouter()
router.register('shop', ShopModelViewSet, 'shop')
router.register('category', CategoryModelViewSet, 'category')
router.register('currency', CurrencyModelViewSet, 'currency')

list_ = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}

urlpatterns = [
    path('', include(router.urls)),
    path('shop/<int:shop>/bot', TelegramBotModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),

    path('shop/<int:shop>/product', ProductModelViewSet.as_view(list_), name='product-list'),
    path('shop/<int:shop>/product/<int:pk>', ProductModelViewSet.as_view(detail), name='product-detail'),
    path('shop/<int:shop>/category', ProductCategoryModelViewSet.as_view(list_), name='product-category-list'),
    path('shop/<int:shop>/category/<int:pk>', ProductCategoryModelViewSet.as_view(detail),
         name='product-category-detail'),
    path('shop/<int:shop>/category/<int:pk>/move', ProductCategoryMoveAPI.as_view(), name='product-category-move'),
    path('shop/<int:shop>/order', OrderModelViewSet.as_view({'get': 'list'}), name='order-list'),
    path('shop/<int:shop>/payment-providers', PaymentProvidersViewSet.as_view(list_),
         name='payment-providers-list'),
    path('shop/<int:shop>/payment-providers/<int:pk>', PaymentProvidersViewSet.as_view(detail),
         name='payment-providers-detail'),

    path('shop/shop/<int:shop>/stat', StatShop.as_view(), name='shop-stat-all'),

]
