from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.serializers import OrderModelSerializer
from products.serializers import CategoryModelSerializer
from shared.mixins import CountResultMixin
from shared.permisions import IsAuthenticatedOwner
from shops.models import Shop
from shops.models.shop_belongs import PaymentProvider
from shops.serializers import ShopSerializer, PaymentSerializers


class ShopModelViewSet(ModelViewSet, CountResultMixin):
    serializer_class = ShopSerializer
    permission_classes = IsAuthenticatedOwner,

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.shop_set.all()
        return Response(status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        return self.count_result_list(request, *args, **kwargs)

    @action(['GET', 'POST'], True, 'category', 'category', serializer_class=CategoryModelSerializer,
            permission_classes=(IsAuthenticatedOwner,))
    def get_create_categories(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        if request.method == 'GET':
            return self.get_count_result_list(shop.categories)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shop=shop)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(['GET'], True, 'order', 'order', serializer_class=OrderModelSerializer)
    def get_orders(self, request, pk):
        shop = get_object_or_404(Shop, pk=pk)
        return self.get_count_result_list(shop.orders)

    @action(['GET'], False, 'shop-config', 'shop-config')
    def shop_config(self, request):
        langs = (("🇺🇿", "O'zbekcha", "uz"), ("🇷🇺", "Русский", "ru"), ("🇺🇸", "English", "en"))
        data = {"languages": [{'icon': i, 'title': t, 'code': c} for i, t, c in langs]}
        return Response(data)


class PaymentProvidersListAPIView(ListAPIView):
    queryset = PaymentProvider.objects.all()
    serializer_class = PaymentSerializers
