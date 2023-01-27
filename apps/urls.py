from django.urls import include, path

urlpatterns = [
    path('shop/', include('shops.urls')),
    path('', include('products.urls')),
    path('', include('users.urls')),
]
