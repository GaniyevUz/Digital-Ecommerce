from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

from shops.models import Shop
from shops.serializers import ShopSerializer


class ShopListCreateAPIView(ListCreateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return self.request.user.shop_set.all()

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        data = {
            'count': self.get_queryset().count(),
            'result': serializer.data
        }
        return Response(data, status.HTTP_200_OK)


class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
