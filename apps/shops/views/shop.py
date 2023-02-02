from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.mixins import CountResultMixin
from shops.models import Shop
from shops.models.shop_belongs import PaymentProviders
from shops.serializers import ShopSerializer, PaymentSerializers


class ShopModelViewSet(ModelViewSet, CountResultMixin):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.shop_set.all()

    @action(methods=['GET'], detail=True, url_name='category', url_path='category')
    def get_category(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        serializer_data = self.serializer_class(shop.category_set.all(), many=True)
        return Response(serializer_data.data)

    def list(self, request, *args, **kwargs):
        return self.count_result_list(request, *args, **kwargs)


class PaymentProvidersListAPIView(ListAPIView):
    queryset = PaymentProviders.objects.all()
    serializer_class = PaymentSerializers
