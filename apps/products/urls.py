from django.urls import path, include

from products.views import ProductModelViewSet, CategoryModelViewSet
from shared.routers import BotCommerceRouter

router = BotCommerceRouter()

router.register('product', ProductModelViewSet, 'product')
router.register('category', CategoryModelViewSet, 'category')

urlpatterns = [
    path('', include(router.urls))
]
