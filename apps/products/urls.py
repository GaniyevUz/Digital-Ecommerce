from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductModelViewSet, CategoryModelViewSet
from shared.routers import BotCommerceRouter

router = DefaultRouter()
# router = BotCommerceRouter()

router.register('product', ProductModelViewSet, 'product')
router.register('category', CategoryModelViewSet, 'category')

urlpatterns = [
    path('ecommerce/<int:shop>/', include(router.urls))
]
