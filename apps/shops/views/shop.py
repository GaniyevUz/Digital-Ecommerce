from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from shops.models import Shop
from shops.serializers import ShopSerializer


class ShopCreateListAPIView(CreateModelMixin, GenericAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return self.request.user.shop_set.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        count = len(queryset)
        if count == 1:
            return Response(serializer.data[0])
        data = {
            'count': count,
            'result': serializer.data
        }
        return Response(data, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, *kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
