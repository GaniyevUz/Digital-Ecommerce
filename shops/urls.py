from django.urls import path

from shops.views.shop import ShopCreateListAPIVIEW

urlpatterns = [
    path('shop/', ShopCreateListAPIVIEW.as_view(), name='shop')
]
