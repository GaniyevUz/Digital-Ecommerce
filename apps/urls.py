from django.urls import path, include

urlpatterns = [
    path('', include(('products.urls', 'products'), 'products')),
    path('ecommerce/<int:shop>/', include('ecommerce.urls'))
]
