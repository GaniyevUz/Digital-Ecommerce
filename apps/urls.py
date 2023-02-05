from django.urls import include, path

urlpatterns = [
    path('shop/', include(('shops.urls', 'shops'), 'shops')),
    path('ecommerce/', include('ecommerce.urls')),
    path('', include('products.urls')),
    path('', include(('users.urls', 'users'), 'users')),

]
