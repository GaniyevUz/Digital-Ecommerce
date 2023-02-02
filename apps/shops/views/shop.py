from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.response import Response

from shops.models import Shop
from shops.models.shop_belongs import PaymentProviders
from shops.serializers import ShopSerializer, PaymentSerializers


class ShopListCreateAPIView(ListCreateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return self.request.user.shop_set.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response = {
            'count': queryset.count(),
            'result': serializer.data
        }
        return Response(response)


class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class Payment_providersListAPIView(ListAPIView):
    queryset = PaymentProviders.objects.all()
    serializer_class = PaymentSerializers
