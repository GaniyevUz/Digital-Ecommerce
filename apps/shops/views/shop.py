from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response

from shops.models import Shop
from shops.serializers import ShopSerializer


class ShopCreateListAPIView(ListCreateAPIView):
    serializer_class = ShopSerializer
    queryset = Shop.objects.all()

    def get_queryset(self):
        return self.request.user.shop_set.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response = {
            'count': queryset.count(),
            'result': serializer.data
        }
        return Response(response)


# class ShopCreateListAPIView(CreateModelMixin, GenericAPIView):
#     serializer_class = ShopSerializer
#
#     def get_queryset(self):
#         return self.request.user.shop_set.all()
#
    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     count = len(queryset)
    #     if count == 1:
    #         return Response(serializer.data[0])
    #     data = {
    #         'count': count,
    #         'result': serializer.data
    #     }
    #     return Response(data, status.HTTP_200_OK)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, *kwargs)
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #

class ShopRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
