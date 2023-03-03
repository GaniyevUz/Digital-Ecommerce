from django.urls import include, path

urlpatterns = [
    path('users/', include(('users.urls', 'users'), 'users')),
    path('shops/', include(('shops.urls', 'shops'), 'shops')),
]
