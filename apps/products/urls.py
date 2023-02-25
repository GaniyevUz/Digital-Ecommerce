from django.urls import path, include

from products.views import ProductModelViewSet, CategoryModelViewSet
from shared.routers import BotCommerceRouter

router = BotCommerceRouter()


urlpatterns = [
    path('product', ProductModelViewSet.as_view({'get': 'list'}), name='product-list'),
    path('product/<int:pk>', ProductModelViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    path('category', CategoryModelViewSet.as_view({'get': 'list'}), name='category'),
    path('category/<int:pk>', CategoryModelViewSet.as_view({'get': 'retrieve'}), name='category'),
    path('', include(router.urls))
]
