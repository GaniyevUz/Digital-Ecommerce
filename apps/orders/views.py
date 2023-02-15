from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from orders.models import Order
from orders.serializers import OrderModelSerializer
from shops.models import Shop


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    pagination_class = None

    def list(self, request, shop, *args, **kwargs):
        shop = get_object_or_404(Shop, pk=shop)
        self.queryset = shop.orders
        return super().list(request, *args, **kwargs)
