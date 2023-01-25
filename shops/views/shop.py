from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView

from shops.models import Shop
from shops.serializers import ShopSerializer


class ShopsCreateListAPIVIEW(CreateAPIView, ListAPIView):
    def get_queryset(self):
        return self.request.user.shop_set

    serializer_class = ShopSerializer


class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
