from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shops.models import Currency, Category, Shop
from shops.models.shop_belongs import PaymentProviders
from shops.serializers import CategorySerializer, CurrencySerializer, PaymentSerializers, OrderSerializer


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]


class CurrencyModelViewSet(ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentProvidersViewSet(ModelViewSet):
    serializer_class = PaymentSerializers
    queryset = PaymentProviders.objects.all()


class ShopOrdersRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrderSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop: Shop = self.get_object()
        return shop.order_set.all()
