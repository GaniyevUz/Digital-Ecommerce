from shared.django import APIViewSet

from orders.models import Order
from orders.serializers import OrderModelSerializer
from shared.django import BaseShopMixin
from shared.restframework import CustomPageNumberPagination


class OrderAPIViewSet(BaseShopMixin, APIViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    pagination_class = CustomPageNumberPagination
