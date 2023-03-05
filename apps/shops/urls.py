from django.urls import path, include

from orders.views import OrderAPIViewSet
from products.views import CategoryAPIViewSet as ProductCategoryAPIViewSet, ProductAPIViewSet
from shared.django import CustomRouter
from shops.views import ShopAPIViewSet, CurrencyAPIViewSet, PaymentProvidersViewSet, CategoryAPIViewSet, StatShop
from shops.views.shop import CountryAPIViewSet, CategoryMoveAPI as ProductCategoryMoveAPI
from shops.views.shop_belongs import TelegramBotAPIViewSet

router_stat = CustomRouter()
router_stat.register('stat', StatShop, 'stat')
router = CustomRouter()
router.register('category', CategoryAPIViewSet, 'category')
router.register('currency', CurrencyAPIViewSet, 'currency')
router.register('countries', CountryAPIViewSet, 'country')

list_ = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}

urlpatterns = [
    path('', include(router.urls)),
    path('shop', ShopAPIViewSet.as_view(list_), name='shop-list'),
    path('shop_config', ShopAPIViewSet.as_view({'get': 'shop-config'}), name='shop-config'),
    path('<int:shop>/detail', ShopAPIViewSet.as_view(detail), name='shop-detail'),
    path('shop/<int:shop>/', include(router_stat.urls)),
    path('<int:shop>/bot', TelegramBotAPIViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}),
         name='telegrambot'),
    path('<int:shop>/product', ProductAPIViewSet.as_view(list_), name='product-list'),
    path('<int:shop>/product/<int:pk>', ProductAPIViewSet.as_view(detail), name='product-detail'),
    path('<int:shop>/category', ProductCategoryAPIViewSet.as_view(list_), name='product-category-list'),
    path('<int:shop>/category/<int:pk>', ProductCategoryAPIViewSet.as_view(detail),
         name='product-category-detail'),
    path('<int:shop>/category/<int:pk>/move', ProductCategoryMoveAPI.as_view(), name='product-category-move'),
    path('<int:shop>/category/<int:pk>/translations', ProductCategoryAPIViewSet.as_view('translations'),
         name='product-category-translations'),
    path('<int:shop>/order', OrderAPIViewSet.as_view({'get': 'list'}), name='order-list'),
    path('<int:shop>/payment-providers', PaymentProvidersViewSet.as_view(list_),
         name='payment-providers-list'),
    path('<int:shop>/payment-providers/<int:pk>', PaymentProvidersViewSet.as_view(detail),
         name='payment-providers-detail'),
    # Todo Conflict
    # path('shop/<int:shop>/stat', StatShop.as_view(), name='shop-stat-all')
]
