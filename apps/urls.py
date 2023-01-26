from django.urls import include, path

urlpatterns = [
    path('', include('shops.urls')),
    path('', include('products.urls')),
]
