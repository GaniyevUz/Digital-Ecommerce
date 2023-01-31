from django.urls import include, path

urlpatterns = [
    path('shop/', include(('shops.urls', 'shops'), 'shops')),
    path('', include('products.urls')),
    path('', include(('users.urls', 'users'), 'users')),

]
