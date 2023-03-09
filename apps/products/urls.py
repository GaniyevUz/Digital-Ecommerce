from django.urls import path, include

from products.views import ProductAPIViewSet, CategoryAPIViewSet
from shared.restframework import CustomRouter

router = CustomRouter()


urlpatterns = [
    path('product', ProductAPIViewSet.as_view({'get': 'list'}), name='product-list'),
    path('product/<int:pk>', ProductAPIViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    path('category', CategoryAPIViewSet.as_view({'get': 'list'}), name='category-list'),
    path('category/<int:pk>', CategoryAPIViewSet.as_view({'get': 'retrieve'}), name='category'),
    path('', include(router.urls))
]
