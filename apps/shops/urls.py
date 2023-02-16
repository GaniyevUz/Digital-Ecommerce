from django.urls import path

from orders.views import OrderModelViewSet
from products.views import CategoryModelViewSet as ProductCategoryModelViewSet, ProductModelViewSet
from shops.views import ShopModelViewSet, CurrencyModelViewSet, PaymentProvidersViewSet, CategoryModelViewSet
from shops.views.shop_belongs import TelegramBotModelViewSet

list_ = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}
urlpatterns = [
    path('shop', ShopModelViewSet.as_view(list_), name='shop-list'),
    path('shop/shop-config', ShopModelViewSet.as_view({'get': 'shop_config'}), name='shop-shop-config'),
    path('shop/category', CategoryModelViewSet.as_view(list_), name='category-list'),
    path('shop/category/<int:pk>', CategoryModelViewSet.as_view(detail), name='category-detail'),
    path('shop/currency', CurrencyModelViewSet.as_view(list_), name='currency-list'),
    path('shop/currency/<int:pk>', CurrencyModelViewSet.as_view(detail), name='currency-detail'),
    path('shop/<int:pk>/detail', ShopModelViewSet.as_view(detail), name='shop-detail'),
    path('shop/<int:shop>/bot', TelegramBotModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),
    path('shop/<int:shop>/product', ProductModelViewSet.as_view(list_), name='product-list'),
    path('shop/<int:shop>/category', ProductCategoryModelViewSet.as_view(list_), name='product-category-list'),
    path('shop/<int:shop>/category/<int:pk>', ProductCategoryModelViewSet.as_view(detail),
         name='product-category-detail'),
    # path('shop/<int:shop>/category/<int:pk>/move', ProductCategoryModelViewSet.as_view({'post': 'move'}),
    #      name='product-category-move'),
    path('shop/<int:shop>/order', OrderModelViewSet.as_view({'get': 'list'}), name='order-list'),
    path('shop/<int:shop>/payment-providers', PaymentProvidersViewSet.as_view(list_),
         name='payment-providers-list'),
    path('shop/<int:shop>/payment-providers/<int:pk>', PaymentProvidersViewSet.as_view(detail),
         name='payment-providers-detail')
]
