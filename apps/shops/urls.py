from django.urls import path

from apps.shops.views.shop import ShopCreateListAPIView

urlpatterns = [
    path('shop/', ShopCreateListAPIView.as_view(), name='shop')
]
