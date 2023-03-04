from django.urls import path, include

from orders.views import OrderAPIViewSet
from products.views import CategoryAPIViewSet as ProductCategoryAPIViewSet, ProductAPIViewSet, \
    ProductCategoryMoveAPI
from shared.django import CustomRouter
from shops.views import ShopAPIViewSet, CurrencyAPIViewSet, PaymentProvidersViewSet, CategoryAPIViewSet, StatShop
from shops.views.shop import CountryAPIViewSet
from shops.views.shop_belongs import TelegramBotAPIViewSet

router_stat = BotCommerceRouter()
router_stat.register('stat', StatShop, 'stat')
router = CustomRouter()
router.register('shop', ShopAPIViewSet, 'shop')
router.register('category', CategoryAPIViewSet, 'category')
router.register('currency', CurrencyAPIViewSet, 'currency')
router.register('countries', CountryAPIViewSet, 'country')

list_ = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}

urlpatterns = [
    path('', include(router.urls)),
    path('shop/<int:shop>', include(router_stat.urls)),
    path('<int:shop>/bot', TelegramBotAPIViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),

    path('<int:shop>/product', ProductAPIViewSet.as_view(list_), name='product-list'),
    path('<int:shop>/product/<int:pk>', ProductAPIViewSet.as_view(detail), name='product-detail'),
    path('<int:shop>/category', ProductCategoryAPIViewSet.as_view(list_), name='product-category-list'),
    path('<int:shop>/category/<int:pk>', ProductCategoryAPIViewSet.as_view(detail),
         name='product-category-detail'),
    path('<int:shop>/category/<int:pk>/move', ProductCategoryMoveAPI.as_view(), name='product-category-move'),
    path('<int:shop>/order', OrderAPIViewSet.as_view({'get': 'list'}), name='order-list'),
    path('<int:shop>/payment-providers', PaymentProvidersViewSet.as_view(list_),
         name='payment-providers-list'),
    path('<int:shop>/payment-providers/<int:pk>', PaymentProvidersViewSet.as_view(detail),
         name='payment-providers-detail'),
]
