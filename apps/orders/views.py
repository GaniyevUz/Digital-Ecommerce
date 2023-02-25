from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import OrderModelSerializer
from shared.mixins import BaseShopMixin
from shared.paginate import CustomPageNumberPagination


class OrderModelViewSet(BaseShopMixin, ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    pagination_class = CustomPageNumberPagination
