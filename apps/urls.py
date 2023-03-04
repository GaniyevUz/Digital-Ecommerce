from django.urls import include, path

urlpatterns = [
    path('', include(('products.urls', 'products'), 'products')),
    path('', include(('ecommerce.urls', 'ecommerce'), 'ecommerce'))
]
