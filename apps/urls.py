from django.urls import include, path

urlpatterns = [
    path('', include(('users.urls', 'users'), 'users')),
    path('shop/', include(('shops.urls', 'shops'), 'shops')),
    path('ecommerce/<int:shop>/', include('ecommerce.urls')),
    path('', include('products.urls')),
]
