from django.urls import path

from shops.views.shop import ShopsCreateListAPIVIEW

urlpatterns = [
    path('shop/', ShopsCreateListAPIVIEW.as_view(), name='shop')
]
