from django.urls import include, path

from products.views import ProductModelViewSet, CategoryModelViewSet

urlpatterns = [
    # path('', include(('products.urls', 'products'), 'products')),
    path('product', ProductModelViewSet.as_view({'get': 'list'}), name='product'),
    path('product/<int:id>', ProductModelViewSet.as_view({'get': 'retrieve'}), name='product'),
    path('category', CategoryModelViewSet.as_view({'get': 'list'}), name='category'),
    path('category/<int:id>', CategoryModelViewSet.as_view({'get': 'retrieve'}), name='category'),
    path('', include('ecommerce.urls'))
]
